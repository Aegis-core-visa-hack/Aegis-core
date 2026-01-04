# AEGIS - Agent Coordination Document
## Cross-Conversation Context for Parallel Development

> **Last Updated:** 2026-01-05 04:30 IST
> **Active Agents:** Backend (separate), UI (separate), **Coordinator (this conversation)**
> **Project:** Visa Hackathon PS4 - Agentic AI Compliance Platform

---

## 1. CURRENT STATE

### What's Done
- [x] Problem statement analysis
- [x] Visa-specific requirements understanding
- [x] Architecture design (5 agents, shared memory) - **v3 complete**
- [x] Tech stack decisions
- [x] UI/UX design decisions
- [x] Pitch deck materials (in `pitch_materials/`)
- [x] Technical documentation (`ARCHITECTURE.md` - 94KB, comprehensive)
- [x] Repository setup (Git init, push to GitHub)
- [x] **Frontend skeleton** - Next.js + shadcn running on localhost:3000

### Frontend Progress (UI Agent)
| Page | Status | Notes |
|------|--------|-------|
| Dashboard (`/`) | ✅ Built | `app/page.tsx` |
| Alerts List (`/alerts`) | ✅ Built | `app/alerts/` |
| Alert Detail (`/alerts/[id]`) | ✅ Built | Currently viewing |
| Chat (`/chat`) | ✅ Built | `app/chat/` |
| Entities (`/entities`) | ✅ Built | `app/entities/` |

**Components Built:** 13+ (dashboard/, alerts/, layout/, ui/)

### What's In Progress
- [ ] Backend implementation (FastAPI, agents) - **Not started**
- [x] Frontend implementation - **In progress, most screens built**

### What's Not Started
- [ ] Backend API implementation
- [ ] Database schema creation (PostgreSQL + pgvector)
- [ ] Agent 3 implementation (Transaction Monitor)
- [ ] Mock data generation (for backend)
- [ ] API integration (frontend → backend)

---

## 2. KEY DECISIONS (With Rationale)

### Tech Stack

| Component | Decision | Why | Alternatives Considered |
|-----------|----------|-----|------------------------|
| LLM | **Gemini Pro/Flash** | Cost-effective, good structured output | GPT-4, Claude |
| Database | **PostgreSQL + pgvector** | Unified relational + vector, ACID | ChromaDB + SQLite (rejected: two systems) |
| Agents | **PydanticAI + LangChain** | Type-safe, RAG support | LangGraph (rejected: overkill) |
| Backend | **FastAPI** | Async, Python ecosystem | Flask, Django |
| Frontend | **Next.js + shadcn/ui** | Modern, component library | React + custom |

### Architecture

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Agent count | 5 specialized agents | Separation of concerns, but manageable |
| Shared memory | Vector DB + Event Bus | Context coherence across agents |
| Detection | 3-layer hybrid (Regex → Semantic → LLM) | Cost/speed optimization |

### UI/UX (IMPORTANT FOR UI AGENT)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Dashboard type | **Static, pre-built components** | Simpler, reliable, covers 80% of needs |
| GenUI | **SKIPPED for MVP** | Too complex, not needed for core demo |
| Chat | **Text-based responses** | Not dynamic UI generation |
| Screens | 4 main screens | Dashboard, Entity Table, Alert Detail, Chat |

---

## 3. PIVOTS & MISTAKES (Learn From These)

### ❌ Things We Tried and Abandoned

#### Pivot 1: Generic vs Visa-Specific
```
BEFORE: Designed for "any financial institution"
- Included GitHub code scanning
- Included Slack message monitoring
- Included Jira ticket creation

AFTER: Redesigned for Visa's actual needs
- Removed code repo monitoring (not Visa's scope)
- Removed internal chat monitoring
- Replaced Jira with GRC workflow systems

WHY PIVOT: Visa is a payment NETWORK, not a bank or software company.
They don't audit member banks' source code.
```

#### Pivot 2: GenUI
```
BEFORE: Planned GenUI - AI generates dynamic UI components

AFTER: Dropped GenUI for MVP

WHY PIVOT:
1. 10x more complex to implement
2. Static dashboards cover 80% of use cases
3. Text-based chat is sufficient
4. Risky for demo (AI-generated UI can break)
```

#### Pivot 3: Multiple Databases
```
BEFORE: ChromaDB for vectors + SQLite for relational data

AFTER: PostgreSQL + pgvector (single database)

WHY PIVOT: One database = simpler ops, unified transactions, better for compliance auditing
```

#### Pivot 4: LangGraph
```
BEFORE: Considered LangGraph for agent orchestration

AFTER: PydanticAI + LangChain

WHY PIVOT: LangGraph is overkill for 5 agents. PydanticAI gives type safety.
```

### ✅ Things That Worked Well
- User persona analysis before UI design
- Problem statement deep-dive before architecture
- Hybrid detection approach (cost/speed tradeoffs)

---

## 4. VISA-SPECIFIC CONTEXT (DON'T LOSE THIS)

### Who is Visa?
- **Payment NETWORK** (not a bank, not a software company)
- Creator of PCI-DSS (they wrote the rules)
- Works with 15,000+ member banks, millions of merchants
- Operates in 200+ countries

### What Visa Monitors (NOT what we initially thought)
| DOES Monitor | DOES NOT Monitor |
|--------------|------------------|
| Transaction patterns | Member bank code repos |
| Member bank compliance status | Internal Slack/Teams |
| Merchant PCI certifications | Developer environments |
| Cross-border data flows | CRM systems |
| Regulatory changes globally | |

### Problem Statement Alignment
> "Create an agentic AI-powered compliance platform built on autonomous, agent-based systems that can make decisions, plan tasks, and operate independently using tools and data, without constant human supervision."

Key requirements from PS4:
1. Autonomous agents (not just assistants)
2. Tool use (agents call APIs, databases)
3. Multi-step reasoning
4. Adapt based on feedback
5. Natural language interaction
6. Audit-ready evidence generation

---

## 5. USER PERSONAS (For UI Design)

### Sarah - Compliance Officer (Primary User)
- Daily monitoring
- Needs: Alerts, investigation details, quick actions
- Pain: Information overload

### James - CCO (Executive User)
- Weekly oversight
- Needs: High-level score, trends, board-ready summaries
- Pain: Can't get straight answers

### David - Relationship Manager
- Manages member bank portfolio
- Needs: Entity status, action items
- Pain: Manual tracking

### Maria - External Auditor
- Periodic audits
- Needs: Evidence, documentation, exports
- Pain: Chasing documents

---

## 6. MVP SCOPE (24-Hour Hackathon)

### P0 - Must Demo
| Feature | Owner | Status |
|---------|-------|--------|
| Transaction Monitor (Agent 3) | Backend | ❌ Not started |
| Dashboard UI | UI Agent | ✅ **Built** |
| Alert Detail UI | UI Agent | ✅ **Built** |
| Chat Interface | UI Agent | ✅ **Built** |
| Entities Page | UI Agent | ✅ **Built** |
| Mock Data (frontend) | UI Agent | ✅ Using mock data |
| Mock Data (backend) | Backend | ❌ Not started |
| Backend API | Backend | ❌ Not started |

### P1 - Should Have
| Feature | Owner | Status |
|---------|-------|--------|
| Agent 1 (Reg Monitor) | Backend | ❌ Not started |
| Agent 2 (Compliance Tracker) | Backend | ❌ Not started |
| Risk Heatmap | UI Agent | ✅ **Built** |
| 2D Heatmap (Criticality × Due Date) | Backend + UI | ❌ Not started |

### P2 - Nice to Have
| Feature | Owner | Status |
|---------|-------|--------|
| Agent 4, 5 | Backend | ❌ Not started |
| PDF Export | Backend | ❌ Not started |
| Chat Orchestrator (real) | Backend | ❌ Not started |

---

## 7. FILE STRUCTURE

```
c:\Users\wasim\OneDrive\Documents\visa_hack\
├── ARCHITECTURE.md           # Full technical design
├── AGENT_COORDINATION.md     # This file
├── UI_CONTEXT.md             # Specific context for UI agent
├── pitch_materials/          # Pitch deck, slides, visuals
│   ├── FINAL_SLIDES.md
│   ├── PRESENTATION_GUIDE.md
│   └── ...
├── backend/                  # FastAPI + agents (TO BE CREATED)
│   ├── agents/
│   ├── api/
│   ├── db/
│   └── ...
└── frontend/                 # Next.js + shadcn
    └── ...
```

---

## 8. API CONTRACT (Backend ↔ Frontend)

### Endpoints UI Agent Should Expect

```
GET  /api/dashboard/summary     → Compliance score, counts, agent status
GET  /api/alerts                → List of alerts (filterable)
GET  /api/alerts/{id}           → Alert detail
GET  /api/entities              → Member banks/merchants (filterable)
GET  /api/entities/{id}         → Entity detail
POST /api/chat                  → Send query, get text response
GET  /api/regulations           → Regulation list
GET  /api/risk-heatmap          → Risk by regulation
```

### Response Shapes (Examples)

```json
// GET /api/dashboard/summary
{
  "compliance_score": 78,
  "score_change": 3,
  "open_violations": 23,
  "critical_alerts": 3,
  "agents": [
    {"id": 1, "name": "Regulatory Intel", "status": "online", "last_run": "2026-01-05T08:00:00Z"}
  ]
}

// POST /api/chat
{
  "query": "Which banks have expiring certifications?"
}
// Response:
{
  "response": "3 banks have certifications expiring within 30 days:\n\n1. **First National** (BNK-1234)...",
  "data": [...],  // Optional structured data
  "actions": ["send_reminders", "view_details"]  // Suggested actions
}
```

---

## 9. OPEN QUESTIONS

1. **Authentication:** Skip for MVP or add basic auth?
2. **Real-time updates:** WebSocket for alerts or polling?
3. **Mock data volume:** How many sample entities/alerts?

---

## 10. SESSION LOGGING TEMPLATE

When another agent works on this project, they should log:

```markdown
## Session Log
Date: YYYY-MM-DD HH:MM
Agent: [Backend/UI/Other]
Conversation ID: [if available]

### Context Documents Used
- [ ] ARCHITECTURE.md - Sections used: ___
- [ ] UI_CONTEXT.md - Helpful sections: ___
- [ ] AGENT_COORDINATION.md - Referenced: ___

### What Was Helpful
- ___

### What Was Missing (Add to coordination docs)
- ___

### Decisions Made This Session
- ___

### Work Completed
- ___

### Handoff Notes for Next Agent
- ___
```

---

*Last Updated: 2026-01-05 04:22 IST by Backend Agent*

## Session Log
Date: 2026-01-05 04:22
Agent: Backend (Setup)
Conversation ID: 39cd13bf-a2d3-437f-8798-8d40f90e4bf9

### Context Documents Used
- [x] AGENT_COORDINATION.md - Referenced: Full file

### Work Completed
- Initialized Git repository
- Created .gitignore
- Pushed to GitHub (Aegis-core-visa-hack/Aegis-core)
- Verified frontend skeleton exists

---

## Session Log
Date: 2026-01-05 04:31
Agent: UI Agent
Conversation ID: 7050b5a7-28d9-4a66-a2c3-711fa1a44aec

### Context Documents Used
- [x] ARCHITECTURE.md - Section 7 (User Interface)
- [x] UI_CONTEXT.md - Helpful: screen mockups, tech stack, mock data spec
- [x] AGENT_COORDINATION.md - Referenced: pivots, MVP scope, API contract

### What Was Helpful
- UI_CONTEXT.md had excellent screen mockups and component specs
- Mock data examples were directly usable
- Dark theme color palette was well-defined

### What Was Missing
- Nothing significant - docs were comprehensive

### Decisions Made This Session
- Used shadcn/ui v4 (compatible with Next.js 16 + Tailwind 4)
- Extracted AlertActions to client component (server component can't have onClick)
- Kept chat as text-based (as per GenUI pivot decision)

### Work Completed
- [x] Dashboard page (`/`) - Metrics, Risk Heatmap, Alerts, Agent Status
- [x] Alerts list (`/alerts`) - Severity badges, status, navigation
- [x] Alert detail (`/alerts/[id]`) - Evidence, recommendations, action buttons
- [x] Chat interface (`/chat`) - Message history, suggested queries, mock responses
- [x] Entities table (`/entities`) - PCI status, risk levels, filters
- [x] Header component with navigation
- [x] All shadcn components installed
- [x] Mock data file (`lib/mockData.ts`)

### Handoff Notes for Next Agent
- **Dev server**: Run `npm run dev` in `/frontend`
- **API Integration**: Replace mock data imports with fetch calls to backend
- **Real-time**: Consider WebSocket for alerts (currently static)
- **Filters**: Entity table has filter UI but no logic yet

---

## Session Log
Date: 2026-01-05 04:33 - 05:00
Agent: Backend Implementation
Conversation ID: 7a2b658f-ef69-43b6-b7e2-ab03f07596d5

### Context Documents Used
- [x] ARCHITECTURE.md - Agent specs, shared memory design
- [x] AGENT_COORDINATION.md - MVP scope, API contract
- [x] reference_repo/logic_specs/*.txt - Database schema, API specs, Agent 3 logic

### What Was Helpful
- Logic specs gave complete API response shapes
- Mock data from frontend ensured compatibility
- Decision to skip auth for hackathon saved time

### Work Completed
- [x] FastAPI backend structure (main.py, routes/, agents/)
- [x] All 4 API route modules (dashboard, alerts, entities, chat)
- [x] Agent 3 Transaction Monitor with PAN detection + Luhn validation
- [x] Demo endpoints for live scanning (/api/demo/scan)
- [x] Gemini integration in chat (with mock fallback)
- [x] Frontend chat page updated to call backend
- [x] Verified end-to-end: chat shows real API responses

### Files Created
- `backend/main.py` - FastAPI app with CORS
- `backend/models.py` - Pydantic models  
- `backend/mock_data.py` - In-memory data
- `backend/routes/dashboard.py` - 4 endpoints
- `backend/routes/alerts.py` - 3 endpoints
- `backend/routes/entities.py` - 2 endpoints
- `backend/routes/chat.py` - Gemini chat
- `backend/routes/demo.py` - Agent 3 demo
- `backend/agents/transaction_monitor.py` - PAN detection
- `frontend/lib/api.ts` - API client (not yet fully used)

### Handoff Notes for Next Agent
- **Backend running**: `cd backend && python -m uvicorn main:app --port 8000`
- **Endpoints verified**: All work via Swagger at http://localhost:8000/docs
- **Chat integrated**: Frontend calls real /api/chat endpoint
- **For Gemini**: Set GEMINI_API_KEY env var (currently uses mock responses)
- **For demo**: POST /api/demo/scan creates live violations

