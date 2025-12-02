# 🏗️ Architecture Overview

## System Design

### Multi-Agent Architecture (LangGraph)

```
┌─────────────────────────────────────────────────────────────┐
│                      User Query                              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Router Agent                               │
│  • Analyzes query intent                                     │
│  • Retrieves relevant context from Qdrant                    │
│  • Routes to appropriate agent                               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Analyzer Agent                             │
│  • Uses PandasAI for data analysis                          │
│  • Executes natural language queries                        │
│  • Returns structured results                               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                Insight Generator Agent                       │
│  • Leverages GPT-4 for business insights                   │
│  • Generates actionable recommendations                     │
│  • Formats results for presentation                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Memory Manager Agent                        │
│  • Stores interaction in Qdrant                             │
│  • Creates embeddings for semantic search                   │
│  • Enables context-aware future queries                     │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. LangGraph Orchestration

**Purpose**: Coordinate multiple specialized agents in a workflow

**Key Features**:
- State management across agents
- Conditional routing based on query type
- Error handling and recovery
- Parallel agent execution when possible

**Implementation**: `agents/orchestrator.py`

### 2. Qdrant Vector Memory

**Purpose**: Store and retrieve contextual information

**Storage Strategy**:
- **Initial Context**: Dataset metadata, column info, sample data
- **Interaction History**: User queries and AI responses
- **Insights Cache**: Generated business insights

**Vector Embeddings**: OpenAI text-embedding-ada-002 (1536 dimensions)

**Search Strategy**:
- Cosine similarity for semantic search
- Top-K retrieval (default: 3-5 results)
- Timestamp-based filtering for recent context

### 3. PandasAI Integration

**Purpose**: Natural language to data analysis

**Capabilities**:
- SQL-like queries in natural language
- Automatic chart generation
- Statistical analysis
- Data transformation

**Example Queries**:
```python
"What are the top 5 products by revenue?"
"Show correlation between discount and sales"
"Plot monthly revenue trends"
```

### 4. Streamlit UI

**Purpose**: Interactive web interface

**Features**:
- File upload (Excel/CSV)
- Real-time chat interface
- Data visualization
- Memory exploration
- Agent status monitoring

## Data Flow

```
Excel/CSV Upload
    ↓
DataFrame Creation
    ↓
Orchestrator Initialization
    ↓
Qdrant Collection Setup
    ↓
User Query → Router → Analyzer → Insight Gen → Memory → Response
    ↑                                              ↓
    └──────────── Context Retrieval ──────────────┘
```

## Key Design Decisions

### Why LangGraph?
- Flexible agent orchestration
- Built-in state management
- Easy to extend with new agents
- Better than simple chains for complex workflows

### Why Qdrant?
- Fast vector similarity search
- Easy Docker deployment
- Rich filtering capabilities
- Persistent storage

### Why PandasAI?
- Natural language interface to pandas
- Reduces code complexity
- Handles complex queries automatically
- Built-in visualization

## Scalability Considerations

1. **Memory Management**: Qdrant can handle millions of vectors
2. **Agent Parallelization**: Independent agents can run concurrently
3. **Caching**: Frequently asked queries cached in memory
4. **Batch Processing**: Large datasets processed in chunks

## Security

- API keys stored in environment variables
- No data persistence beyond session (optional)
- Qdrant can be configured with authentication
- Input sanitization for SQL injection prevention

## Future Enhancements

- [ ] Multi-file analysis
- [ ] Custom agent creation
- [ ] Advanced visualization agents
- [ ] Export reports to PDF
- [ ] Scheduled insight generation
- [ ] Multi-user support with separate collections
