# 🤖 PandasAI Agentic Insights

An intelligent multi-agent system for business data analysis powered by LangGraph, Qdrant vector memory, and PandasAI.

## 🌟 Features

- **Multi-Agent Architecture**: LangGraph orchestrates specialized agents (Router, Analyzer, Insight Generator, Memory Manager)
- **Vector Memory**: Qdrant stores and retrieves contextual information from past interactions
- **Natural Language Queries**: Ask questions in plain English using PandasAI
- **Interactive UI**: Beautiful Streamlit interface for data exploration
- **Auto-Insights**: AI-generated business insights and recommendations
- **Memory Search**: Query past analyses and build on previous insights

## 🏗️ Architecture

```
User Query → Router Agent → Analyzer Agent (PandasAI) → Insight Generator → Memory Manager (Qdrant) → Response
                ↑                                                                      ↓
                └──────────────────── Context Retrieval ────────────────────────────┘
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.9+
- Docker (for Qdrant)
- OpenAI API Key

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/inamdarmihir/pandasai-agentic-insights.git
cd pandasai-agentic-insights

# Install dependencies
pip install -r requirements.txt
```

### 3. Setup Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

### 4. Start Qdrant

```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

### 5. Generate Sample Data (Optional)

```bash
python utils/data_generator.py
```

### 6. Run the App

```bash
streamlit run app.py
```

Visit `http://localhost:8501` in your browser!

## 💡 Usage Examples

### Natural Language Queries

- "What are the top 5 products by revenue?"
- "Show me sales trends over time"
- "Which region has the highest profit margin?"
- "Calculate average customer satisfaction by product"
- "Find correlations between discount and revenue"

### Auto-Insights

Click the "Auto Insights" button to get AI-generated business recommendations based on your data.

## 🧠 How It Works

1. **Router Agent**: Receives your query and retrieves relevant context from Qdrant memory
2. **Analyzer Agent**: Uses PandasAI to execute data analysis and generate results
3. **Insight Generator**: Leverages GPT-4 to create actionable business insights
4. **Memory Manager**: Stores the interaction in Qdrant for future context-aware responses

## 📊 Sample Datasets

The project includes generators for:
- **Sales Data**: Products, regions, revenue, profit, customer satisfaction
- **HR Data**: Employees, departments, salaries, performance metrics

## 🛠️ Tech Stack

- **LangGraph**: Agent orchestration and workflow management
- **Qdrant**: Vector database for semantic memory
- **PandasAI**: Natural language data analysis
- **OpenAI GPT-4**: Language understanding and insight generation
- **Streamlit**: Interactive web interface
- **Plotly**: Data visualization

## 📁 Project Structure

```
pandasai-agentic-insights/
├── app.py                      # Streamlit UI
├── agents/
│   ├── __init__.py
│   └── orchestrator.py         # LangGraph agent system
├── utils/
│   ├── __init__.py
│   └── data_generator.py       # Sample data generators
├── requirements.txt
├── .env.example
└── README.md
```

## 🔧 Configuration

Edit `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=http://localhost:6333
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

MIT License

## 🙏 Acknowledgments

- LangGraph for agent orchestration
- Qdrant for vector memory
- PandasAI for natural language data analysis
- OpenAI for language models

---

Built with ❤️ by [Mihir Inamdar](https://github.com/inamdarmihir)
