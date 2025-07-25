# 📈 PortfolioPilot AI

**PortfolioPilot AI** is an intelligent, multi-agent financial chatbot that securely connects to your live Zerodha account. It leverages a sophisticated backend using **LangGraph** to orchestrate specialized AI agents, **OpenAI** for language understanding, and provides a real-time conversational UI with **Streamlit**.

---

## 🚀 Features

### 🧠 Interactive Financial Analysis  
Run the web application, securely log in to your Zerodha account, and ask complex financial questions in plain English.

### 🧩 Intelligent Multi-Agent Framework  
Built with LangGraph to create a robust workflow that intelligently routes your request to the best-specialized agent for the job:

- **📊 Portfolio Agent** – Connects to your live Zerodha account to fetch holdings and positions.
- **🌐 Market Research Agent** – Explores real-time news and market data using the Tavily search API.
- **⚠️ Risk Analyst** – Intelligently assesses portfolio diversification and sector concentration.
- **📈 Technical Analyst** – Calculates key indicators like RSI from historical stock data and uses real-time data for analysis.

### 🔁 Stateful & Context-Aware  
The bot remembers the full context of your conversation, allowing for natural follow-up questions (e.g., “what are the risks in that sector?”)

### 📡 Data-Driven & Reliable  
Agents are grounded with strict prompts to base their answers on factual data from APIs, reducing LLM hallucinations.

### 💻 User-Friendly Web Interface  
A clean UI built with Streamlit that handles secure authentication flow and provides a seamless chat experience.

---

## 🛠️ Technology Stack

| Layer              | Tech Used               |
|--------------------|--------------------------|
| **Orchestration**  | LangGraph                |
| **Language Model** | OpenAI (GPT-4o-mini)     |
| **Web Interface**  | Streamlit                |
| **Broker API**     | Zerodha Kite Connect     |
| **Web Search**     | Tavily AI                |
| **Stock Data**     | yfinance, Tavily Search  |
| **Package Manager**| uv                       |

---

## ⚙️ Prerequisites

### 🖥️ System
- Python **3.11+**
- `uv` (recommended Python package manager)
- `graphviz` (for agent graph visualization)

### 🔑 API Keys
Create a `.env` file in the root of the project with the following keys:

```env
# Required for agent functionality
OPENAI_API_KEY="sk-..."
TAVILY_API_KEY="tvly-..."

# Required for live broker connection
ZERODHA_API_KEY="your_zerodha_api_key"
ZERODHA_API_SECRET="your_zerodha_api_secret"
```

---

## 🧰 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/PortfolioPilot-AI.git
cd PortfolioPilot-AI
```

> Replace `your-username` with your actual GitHub username.

---

### 2️⃣ Create the Environment File

```bash
touch .env
```

Populate `.env` with your API keys (see above).

---

### 3️⃣ Setup Backend with `uv`

```bash
# Create the virtual environment
uv venv

# Activate the environment
# On Windows (PowerShell):
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
```

---

## ▶️ Usage

### 1️⃣ Run the Application

```bash
streamlit run app.py
```

---

### 2️⃣ Log In and Interact

- Your browser will open with the PortfolioPilot AI login screen.
- Follow the instructions to log in via Zerodha.
- You will be redirected to a URL with a `request_token`.
- Paste that token back into the Streamlit app.

---

### ✅ Welcome to PortfolioPilot AI!

```text
🔗 Please log in using this URL:
https://kite.zerodha.com/connect/login?api_key=...

🔑 Please paste the request_token here:
[_________________]
```
