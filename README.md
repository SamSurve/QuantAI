<div align="center">
  <h1>📈 QuantAI</h1>
  <h3>Financial Intelligence. Clear Evidence. Better Decisions.</h3>
  <p>AI-powered financial research platform — market data, company analysis and technical signals in one clean workspace.</p>

  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/Agno-AgentOS-6C47FF?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white"/>
</div>

---

## ✨ Features

| | Feature | What it does |
|---|---|---|
| 📊 | **Market Intelligence** | Prices, history, volume and technical indicators |
| 🏢 | **Company Deep Analysis** | Fundamentals, financials and valuation |
| ⚖️ | **Company Comparison** | Side-by-side comparison of multiple companies |
| 📡 | **Technical Signals** | Deterministic market signals |
| 📰 | **News & Events** | Company news and corporate events |
| 🧠 | **AI Research Briefs** | Structured, AI-generated insights |
| 💬 | **Research Assistant** | Chat with the Agno AgentOS research desk |

---

## 🔄 How It Works

```mermaid
flowchart TB
    USER(["👤 User"])
    UI["🖥️ QuantAI Dashboard<br/>Jinja2 · HTMX"]
    API["⚡ FastAPI Backend"]
    ENGINE["🧭 Research Orchestration"]

    USER --> UI --> API --> ENGINE

    subgraph RESEARCH["RESEARCH MODULES"]
        direction LR
        MARKET["📊 Market<br/>Intelligence"]
        COMPANY["🏢 Company<br/>Analysis"]
        SIGNALS["📡 Technical<br/>Signals"]
        COMPARE["⚖️ Company<br/>Comparison"]
    end

    ENGINE --> MARKET
    ENGINE --> COMPANY
    ENGINE --> SIGNALS
    ENGINE --> COMPARE

    MARKET --> DATA["🗂️ Structured Financial Data"]
    COMPANY --> DATA
    SIGNALS --> DATA
    COMPARE --> DATA

    DATA --> AGNO["🤖 Agno AgentOS"]

    subgraph PROVIDERS["AI PROVIDERS · SEQUENTIAL FAILOVER"]
        direction TB
        GROQ1["Groq · Primary"]
        GROQ2["Groq · Secondary"]
        OPENROUTER["OpenRouter · Fallback"]

        GROQ1 -.->|"If unavailable"| GROQ2
        GROQ2 -.->|"If unavailable"| OPENROUTER
    end

    AGNO --> GROQ1

    GROQ1 -->|"Success"| BRIEF["📝 AI Research Brief"]
    GROQ2 -->|"Success"| BRIEF
    OPENROUTER -->|"Success"| BRIEF

    BRIEF --> OUTPUT(["📈 Financial Insights<br/>Chart.js"])

    classDef endpoint fill:#171a21,color:#ffffff,stroke:#64748b,stroke-width:1.5px
    classDef core fill:#263b55,color:#ffffff,stroke:#527ba8,stroke-width:1.5px
    classDef module fill:#f1f5f9,color:#172033,stroke:#94a3b8,stroke-width:1px
    classDef data fill:#e0e7ff,color:#243b70,stroke:#818cf8,stroke-width:1px
    classDef provider fill:#202833,color:#ffffff,stroke:#64748b,stroke-width:1px
    classDef result fill:#20543d,color:#ffffff,stroke:#4c9b74,stroke-width:1.5px

    class USER,OUTPUT endpoint
    class UI,API,ENGINE,AGNO core
    class MARKET,COMPANY,SIGNALS,COMPARE module
    class DATA data
    class GROQ1,GROQ2,OPENROUTER provider
    class BRIEF result
```

---

## 🧰 Tech Stack

| Layer | Tools |
|---|---|
| **Backend** | Python 3.12 · FastAPI · Pydantic · Agno AgentOS |
| **Frontend** | Jinja2 · HTMX · Vanilla JS · Chart.js 4 · Tailwind CSS |
| **AI** | Groq (primary + secondary) · OpenRouter (fallback) |
| **Deployment** | Vercel · Python 3.12 |

---

## 🛡️ Security & Reliability

- 🔒 SSRF protection — private, loopback and cloud-metadata addresses blocked.
- 🔑 API keys stay server-side.
- 🔁 Automatic AI provider failover.
- 🚦 Rate limiting and concurrency protection.
- ⚡ TTL caching and single-flight request coalescing.

---

## 🚀 Quick Start

```powershell
# 1. Clone
git clone https://github.com/SamSurve/QuantAI.git
cd QuantAI

# 2. Virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Install dependencies
python -m pip install -r requirements.txt

# 4. Configure environment
# Copy .env.example to .env and add your API keys.

# 5. Run
uvicorn index:app --port 8000 --host 127.0.0.1 --reload
```

Run tests:

```powershell
python -m pytest -q
```

---

## ⚙️ Environment Variables

| Variable | Purpose |
|---|---|
| `GROQ_API_KEY_PRIMARY` / `GROQ_MODEL_PRIMARY` | Primary AI provider |
| `GROQ_API_KEY_SECONDARY` / `GROQ_MODEL_SECONDARY` | Secondary Groq failover |
| `OPENROUTER_API_KEY` / `OPENROUTER_MODEL` | Fallback provider |
| `AI_PROVIDER_ORDER` | Provider priority |
| `QUANTAI_DEVTOOLS` | Debug telemetry — keep **off** in production |

> ⚠️ Never commit `.env` files or expose API keys in client-side code.

---

## ✅ Quality

**364** automated tests passed · **21** UI features audited · **7** infrastructure/security capabilities verified · Ruff clean · Desktop, mobile, Light and Dark themes tested.

---

## 📚 Documentation

[Feature Checklist](PARITY_CHECKLIST.md) · [Deployment Guide](VERCEL_DEPLOYMENT.md)

---

<div align="center">
  <strong>QuantAI — Making financial research clearer, more structured and easier to understand.</strong>
</div>
