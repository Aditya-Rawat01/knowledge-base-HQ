# Stock Analyzer Agent 📈🤖

A powerful AI-driven financial analyst agent built with **FastAPI**, **LangGraph**, and **Groq**. This agent provides real-time stock market insights, sentiment analysis, and precise financial calculations by orchestrating multiple tools and LLMs.

## 🚀 Features

- **Real-Time Data**: Fetches up-to-date stock information (Price, PE Ratio, Market Cap, etc.) using `yfinance`.
- **Market Sentiment**: A dedicated sub-agent analyzes recent news to provide a sentiment score (Bullish/Bearish) and summary.
- **Smart Ticker Search**: Automatically identifies stock symbols for US (e.g., AAPL) and Indian (e.g., RELIANCE.NS) markets.
- **Precise Calculations**: Uses `numexpr` for mathematical operations, ensuring the LLM doesn't hallucinate numbers.
- **Agentic Workflow**: Powered by **LangGraph** to handle state, tool calling loops, and decision making.
- **FastAPI Interface**: Exposes a clean REST API for integration.

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Orchestration**: LangGraph & LangChain
- **LLM Provider**: Groq (Model: `openai/gpt-oss-120b`)
- **Data Source**: Yahoo Finance (`yfinance`)
- **Package Manager**: uv

## 📋 Prerequisites

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) (Recommended) or pip
- API Keys for Groq

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/stock-analyzer-agent.git
   cd stock-analyzer-agent
   ```

2. **Set up Environment Variables**
   Create a `.env` file in the root directory:
   ```bash
   touch .env
   ```
   Add the following keys (you can get these from the [Groq Console](https://console.groq.com/)):
   ```env
   GROQ_API_KEY_MAIN_AGENT=your_groq_api_key_here
   GROQ_API_KEY_SUB_AGENT=your_groq_api_key_here
   ```

3. **Install Dependencies**
   Using `uv` (based on your Makefile):
   ```bash
   uv sync
   ```
   Or using standard `pip`:
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Usage

### Running the Server
You can use the provided Makefile to start the development server:

```bash
make dev
```
*Alternatively: `uv run fastapi dev main.py`*

The server will start at `http://127.0.0.1:8000`.

### API Endpoints

#### 1. Check Health
**GET** `/`
```json
{
  "msg": "hello from fastapi server!"
}
```

#### 2. Get Stock Insights
**POST** `/stock-data`

Analyze a specific stock or ask a financial question.

**Request Body:**
```json
{
  "query": "How is Apple performing today and what is the sentiment?"
}
```

**Response:**
```json
{
  "msg": "Bottom Line: Apple (AAPL) is showing ... [Detailed analysis, data, and sentiment]"
}
```

### Example via cURL
```bash
curl -X POST "http://127.0.0.1:8000/stock-data" \
     -H "Content-Type: application/json" \
     -d '{"query": "Analyze Reliance Industries and calculate its potential 5% growth"}'
```

## 🧠 Architecture

The project uses a **StateGraph** workflow:

1. **Input**: User query via API.
2. **Main Agent**:
   - Determines if it needs to fetch data, search for a ticker, or calculate values.
   - Enforces "No Mental Math" rules by delegating arithmetic to the Calculator Tool.
3. **Tools**:
   - `get_stock_data`: Fetches raw financial metrics.
   - `search_ticker`: Resolves company names to symbols (handles NS/BO suffixes for India).
   - `get_sentiment`: Spawns a **Sub-Agent** that reads news and outputs structured sentiment data.
   - `calculate`: Safely evaluates math expressions.
4. **Output**: Synthesized natural language response.

## 📂 Project Structure

```text
├── agents/
│   ├── main_agent.py       # LLM configuration for the router/main agent
│   └── subagent.py         # Structured output LLM for sentiment analysis
├── prompts/
│   └── main_agent_prompt.py # System instructions
├── tools/
│   ├── get_company_insights.py
│   ├── calculator.py       # for calculations
│   ├── tools_export.py     # Aggregates tools for the agent
│   └── ...                 # Individual tool definitions

├── main.py                 # FastAPI entry point
├── workflow.py             # LangGraph state machine definition
├── Makefile                # Shortcut commands
├── pyproject.toml          # Project metadata and dependencies
└── README.md
```