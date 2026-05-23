# Sales Dashboard — AI-Powered Analytics App

An interactive sales analytics dashboard built with Python, featuring an AI chat interface that answers questions about your data in plain English.

## Live Demo
[Open the app](https://salesdashboard-ec7thm9fttsdvv4rlx4pja.streamlit.app)

## Features
- Interactive filters by city, month, and product
- KPI metric cards — total orders, revenue, avg order value
- Live charts — revenue by product, month, and city
- Download filtered data as CSV
- AI chat powered by Groq LLaMA 3 — ask anything about your sales data

## Tech Stack
- Python
- Streamlit — web app framework
- Pandas — data manipulation
- LangChain + Groq — AI chat interface
- GitHub + Streamlit Cloud — deployment

## How to run locally

1. Clone the repo
   git clone https://github.com/Deepanshu9650/sales_dashboard.git
   cd sales_dashboard

2. Install dependencies
   pip install -r requirements.txt

3. Add your Groq API key in a .streamlit/secrets.toml file
   GROQ_API_KEY = "your_key_here"

4. Run the app
   streamlit run app.py

## Project structure
- app.py — main Streamlit application
- sales_data.csv — sample sales dataset (200 orders)
- requirements.txt — Python dependencies

## Sample questions to ask the AI
- "Which product made the most revenue?"
- "What was the best month for sales?"
- "How many Electronics orders were there?"
- "What is the average order value in Mumbai?"
