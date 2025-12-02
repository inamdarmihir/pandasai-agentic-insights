#!/bin/bash

echo "🚀 Starting PandasAI Agentic Insights..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env and add your OPENAI_API_KEY"
    exit 1
fi

# Check if Qdrant is running
if ! curl -s http://localhost:6333 > /dev/null; then
    echo "⚠️  Qdrant is not running!"
    echo "Start it with: docker run -p 6333:6333 qdrant/qdrant"
    exit 1
fi

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Generate sample data if not exists
if [ ! -f "sample_sales_data.xlsx" ]; then
    echo "📊 Generating sample data..."
    python utils/data_generator.py
fi

# Start Streamlit
echo "✨ Launching app..."
streamlit run app.py
