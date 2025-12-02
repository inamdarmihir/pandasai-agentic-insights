from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import HumanMessage, AIMessage
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI as PandasOpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import os
from datetime import datetime
import uuid

class AgentState(TypedDict):
    messages: list
    data: pd.DataFrame
    query: str
    analysis_result: str
    insights: list
    next_action: str

class DataInsightOrchestrator:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
        self.embeddings = OpenAIEmbeddings()
        
        # PandasAI setup
        pandas_llm = PandasOpenAI(api_token=os.getenv("OPENAI_API_KEY"))
        self.smart_df = SmartDataframe(df, config={"llm": pandas_llm, "verbose": False})
        
        # Qdrant setup
        self.qdrant = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))
        self.collection_name = f"data_insights_{uuid.uuid4().hex[:8]}"
        self._setup_qdrant()
        
        # Build LangGraph
        self.graph = self._build_graph()
    
    def _setup_qdrant(self):
        """Initialize Qdrant collection"""
        try:
            self.qdrant.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
            )
            
            # Store initial data context
            context = f"Dataset with {len(self.df)} rows and {len(self.df.columns)} columns. Columns: {', '.join(self.df.columns)}"
            embedding = self.embeddings.embed_query(context)
            
            self.qdrant.upsert(
                collection_name=self.collection_name,
                points=[PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload={"text": context, "type": "context", "timestamp": datetime.now().isoformat()}
                )]
            )
        except Exception as e:
            print(f"Qdrant setup warning: {e}")
    
    def _build_graph(self):
        """Build LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("router", self.router_agent)
        workflow.add_node("analyzer", self.analyzer_agent)
        workflow.add_node("insight_generator", self.insight_agent)
        workflow.add_node("memory_manager", self.memory_agent)
        
        # Define edges
        workflow.set_entry_point("router")
        workflow.add_edge("router", "analyzer")
        workflow.add_edge("analyzer", "insight_generator")
        workflow.add_edge("insight_generator", "memory_manager")
        workflow.add_edge("memory_manager", END)
        
        return workflow.compile()
    
    def router_agent(self, state: AgentState) -> AgentState:
        """Route queries and retrieve relevant memory"""
        query = state["query"]
        
        # Search memory for context
        try:
            query_embedding = self.embeddings.embed_query(query)
            search_results = self.qdrant.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=3
            )
            
            context = "\n".join([r.payload.get("text", "") for r in search_results])
            state["messages"].append(HumanMessage(content=f"Context from memory: {context}"))
        except:
            pass
        
        state["messages"].append(HumanMessage(content=query))
        state["next_action"] = "analyze"
        return state
    
    def analyzer_agent(self, state: AgentState) -> AgentState:
        """Analyze data using PandasAI"""
        query = state["query"]
        
        try:
            # Use PandasAI for analysis
            result = self.smart_df.chat(query)
            state["analysis_result"] = str(result)
        except Exception as e:
            state["analysis_result"] = f"Analysis error: {str(e)}"
        
        return state
    
    def insight_agent(self, state: AgentState) -> AgentState:
        """Generate business insights"""
        analysis = state["analysis_result"]
        query = state["query"]
        
        prompt = f"""Based on this data analysis:
Query: {query}
Result: {analysis}

Data context:
- Shape: {self.df.shape}
- Columns: {', '.join(self.df.columns)}
- Sample: {self.df.head(2).to_dict()}

Provide actionable business insights in a clear, concise format."""
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        state["insights"] = [response.content]
        
        return state
    
    def memory_agent(self, state: AgentState) -> AgentState:
        """Store interaction in Qdrant memory"""
        query = state["query"]
        insights = state["insights"]
        
        try:
            # Create memory entry
            memory_text = f"Query: {query}\nInsights: {' '.join(insights)}"
            embedding = self.embeddings.embed_query(memory_text)
            
            self.qdrant.upsert(
                collection_name=self.collection_name,
                points=[PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload={
                        "text": memory_text,
                        "query": query,
                        "type": "interaction",
                        "timestamp": datetime.now().isoformat()
                    }
                )]
            )
        except Exception as e:
            print(f"Memory storage warning: {e}")
        
        return state
    
    def run(self, query: str) -> str:
        """Execute the agent workflow"""
        initial_state = {
            "messages": [],
            "data": self.df,
            "query": query,
            "analysis_result": "",
            "insights": [],
            "next_action": ""
        }
        
        result = self.graph.invoke(initial_state)
        
        # Format response
        response = f"**Analysis:** {result['analysis_result']}\n\n**Insights:**\n{result['insights'][0]}"
        return response
    
    def get_memory_stats(self) -> dict:
        """Get memory statistics"""
        try:
            collection_info = self.qdrant.get_collection(self.collection_name)
            return {
                "collection_name": self.collection_name,
                "vectors_count": collection_info.vectors_count,
                "total_points": collection_info.points_count
            }
        except:
            return {"collection_name": self.collection_name, "vectors_count": 0, "total_points": 0}
    
    def search_memory(self, query: str, limit: int = 5) -> list:
        """Search memory for past interactions"""
        try:
            query_embedding = self.embeddings.embed_query(query)
            results = self.qdrant.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit
            )
            return [r.payload.get("text", "") for r in results]
        except:
            return []
