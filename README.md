# AEGIS - Autonomous Enterprise Governance & Intelligence System

> 🏆 **Visa Hackathon 2025** - Problem Statement 4:  Agentic AI for Compliance

An agentic AI platform that provides continuous PCI/PII compliance monitoring for financial services organizations using a multi-agent architecture with algorithmic orchestration.

![Python](https://img.shields.io/badge/Python-FastAPI-blue)
![Next.js](https://img.shields.io/badge/Frontend-Next.js-black)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🎯 Problem Statement

Financial services operate in a dynamic regulatory environment: 
- **100+ regulations** across jurisdictions
- **~40 regulatory changes/year**
- **80% of violations** found reactively during audits
- **$270B spent annually** on compliance globally

**AEGIS transforms compliance from MANUAL → AUTOMATED, REACTIVE → PROACTIVE**

---

## 🏗️ Architecture Overview

### Multi-Agent System with Algorithmic Orchestration

> ⚠️ **Terminology Note**: This project contains two distinct concepts of "agents":
> - **AEGIS Compliance Agents** (5 specialized AI agents) - The core product that monitors compliance
> - **AI Coding Assistants** (Anthropic Claude, v0) - Tools used during development via platforms like Cursor/Windsurf to accelerate implementation
>
> This README focuses on the **AEGIS Compliance Agents** - the product we built. 

Unlike typical LLM-powered orchestrators, AEGIS uses a **deterministic algorithmic orchestrator** that coordinates specialized compliance agents.  This design choice provides: 

- **Predictable workflow execution** - No LLM hallucination in critical control flow
- **Parallel agent execution** - Compliance agents work independently when possible
- **Event-driven triggers** - Cron jobs and flags trigger agent actions, not an AI deciding when to act

```
┌─────────────────────────────────────────────────────────────────┐
│                    ALGORITHMIC ORCHESTRATOR                      │
│         (Deterministic flow logic, not LLM-powered)             │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  Compliance   │   │  Compliance   │   │  Compliance   │
│   Agent 1     │   │   Agent 2     │   │   Agent 3     │
│  Regulatory   │   │  Ecosystem    │   │  Transaction  │
│  Intelligence │   │   Tracker     │   │   Monitor     │
│  (LLM-powered)│   │ (Rule Engine) │   │ (Regex+Stats) │
└───────────────┘   └───────────────┘   └───────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              ▼
                    ┌───────────────┐
                    │ Shared Memory │
                    │  (pgvector)   │
                    └───────────────┘
                              │
        ┌─────────────────────┴─────────────────────┐
        ▼                                           ▼
┌───────────────┐                         ┌───────────────┐
│  Compliance   │                         │  Compliance   │
│   Agent 4     │                         │   Agent 5     │
│    Cross-     │                         │   Evidence    │
│ Jurisdiction  │                         │   & Reports   │
└───────────────┘                         └───────────────┘
```

### The 5 AEGIS Compliance Agents

| Agent | Purpose | Detection Method |
|-------|---------|------------------|
| **Regulatory Intelligence** | Monitor regulatory landscape, interpret changes | Web scraping + LLM interpretation |
| **Ecosystem Compliance** | Track member banks, merchants, vendors | Rule engine + SQL queries |
| **Transaction Monitor** | Detect PCI violations in transaction data | Regex (PAN) + Statistical anomaly |
| **Cross-Jurisdiction** | Analyze multi-region compliance | Rule lookup + LLM reasoning |
| **Evidence & Reporting** | Generate audit-ready outputs | Template engine + LLM narrative |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **LLM** | Gemini Pro/Flash |
| **Database** | PostgreSQL + pgvector |
| **Agent Framework** | PydanticAI |
| **Backend** | FastAPI (Python) |
| **Frontend** | Next.js + shadcn/ui + Tailwind CSS |
| **Deployment** | Azure Web Apps |

---

## 📁 Repository Structure

```
Aegis-core/
├── backend/
│   ├── agents/                 # Compliance Agent implementations
│   │   ├── regulatory_monitor.py
│   │   ├── ecosystem_tracker.py
│   │   ├── transaction_monitor.py
│   │   ├── cross_jurisdiction. py
│   │   └── evidence_engine.py
│   ├── routes/                 # API endpoints
│   │   ├── alerts.py
│   │   ├── chat.py
│   │   ├── dashboard.py
│   │   └── ... 
│   ├── models. py               # Pydantic models
│   ├── mock_data. py            # Demo data
│   └── main.py                 # FastAPI app
├── frontend/
│   ├── app/                    # Next.js app router
│   ├── components/             # React components
│   │   ├── dashboard/
│   │   ├── alerts/
│   │   └── ui/                 # shadcn components
│   └── lib/
├── pitch_materials/            # Presentation assets
├── ARCHITECTURE.md             # Detailed technical design
├── AGENT_COORDINATION.md       # Agent interaction patterns
└── UI_CONTEXT.md               # UI/UX specifications
```

> ⚠️ **Note on Documentation Files**: This repository contains extensive markdown documentation (`ARCHITECTURE.md`, `AGENT_COORDINATION.md`, `UI_CONTEXT. md`, etc.) that served as **context documents for AI-assisted development** and team coordination during the hackathon.  These are collaboration artifacts, not user-facing documentation. 

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node. js 18+
- PostgreSQL (optional - uses mock data for demo)

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The dashboard will be available at `http://localhost:3000`

---

## 🎥 Demo Features

- **Compliance Dashboard** - Real-time compliance score, risk heatmap, agent status
- **GenUI Chat** - Natural language queries about compliance ("Which banks have expiring PCI certs?")
- **Alert Management** - Prioritized compliance alerts with criticality scoring
- **Entity Tracking** - Member bank and merchant compliance status
- **Cross-Jurisdiction Analysis** - Multi-region transaction compliance checks

---

## 👥 Team & Contributions

This was a collaborative hackathon project with work split across two repositories:

### This Repository (Aegis-core)
| Focus Area | Details |
|------------|---------|
| System Architecture | Comprehensive technical design documentation |
| UI/UX Specifications | Detailed interface design and user flows |
| Frontend Implementation | Next.js dashboard with shadcn/ui components |
| Pitch Materials | Presentation deck and visual assets |
| Mock Data | Realistic demo data for compliance scenarios |
| Agent Scaffolding | Initial compliance agent structure and interfaces |

### Teammate's Repository ([project_aegis](https://github.com/therobinsonscreations/project_aegis))
| Focus Area | Details |
|------------|---------|
| Database Integration | PostgreSQL + pgvector setup and schema |
| Complete Agent Implementation | Full PydanticAI compliance agents |
| Criticality Scoring Model | XGBoost trained on synthetic data for urgency scoring |
| Backend Services | Separate API and service modules |
| Cloud Deployment | Azure Web Apps with production configuration |
| JWT Authentication | Secure login and session management |
| Jira Integration | Ticket creation for compliance violations |
| Additional Features | Member banks, violations tracking, regulations browser |

> 📍 **Live Demo**: The deployed solution is available via the [project_aegis](https://github.com/therobinsonscreations/project_aegis) repository.

---

## 📚 Documentation

- [Architecture Document](./ARCHITECTURE.md) - Comprehensive technical design
- [Agent Coordination](./AGENT_COORDINATION.md) - How compliance agents communicate
- [UI Context](./UI_CONTEXT.md) - Frontend design specifications

---

## 📄 License

MIT License - See [LICENSE](./LICENSE) for details. 
