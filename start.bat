@echo off
echo 🚀 Starting PandasAI Agentic Insights...

REM Check if .env exists
if not exist .env (
    echo ⚠️  .env file not found. Creating from template...
    copy .env.example .env
    echo 📝 Please edit .env and add your OPENAI_API_KEY
    exit /b 1
)

REM Check if virtual environment exists
if not exist venv (
    echo 📦 Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

REM Generate sample data if not exists
if not exist sample_sales_data.xlsx (
    echo 📊 Generating sample data...
    python utils\data_generator.py
)

REM Start Streamlit
echo ✨ Launching app...
streamlit run app.py
