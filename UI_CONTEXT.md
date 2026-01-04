# AEGIS - UI Implementation Context
## Specific Context for Frontend/UI Agent

> **READ FIRST:** This document is specifically for the agent implementing the UI.
> **Also Read:** `ARCHITECTURE.md` (Section 7 - User Interface) and `AGENT_COORDINATION.md`

---

## 1. YOUR MISSION

Build a **fast mockup** that:
1. ✅ Works for demo (looks good, core flows functional)
2. ✅ Clean code (KISS principle)
3. ✅ Production-ready base (no refactoring needed later)
4. ❌ NOT over-engineered
5. ❌ NOT pixel-perfect (demo quality, not production polish)

---

## 2. TECH STACK (Already Decided)

| Layer | Technology | Notes |
|-------|------------|-------|
| Framework | **Next.js 14+** | App router |
| Components | **shadcn/ui** | Use pre-built components |
| Styling | **Tailwind CSS** | Via shadcn |
| State | **React hooks** | Keep simple, no Redux |
| API | **Fetch** | Backend at `http://localhost:8000` |

### Don't Use
- Redux/Zustand (overkill for MVP)
- Styled-components (Tailwind is sufficient)
- D3.js (use simple charts or skip)
- Any complex state management

---

## 3. SCREENS TO BUILD (Priority Order)

### Screen 1: Dashboard (P0 - MUST HAVE)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  AEGIS                                          [Ask AEGIS] [Settings]  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐                │
│  │     78%       │  │     23        │  │     3         │                │
│  │  Compliance   │  │  Open         │  │  Critical     │                │
│  │  Score        │  │  Violations   │  │  Alerts       │                │
│  │  ▲ +3%        │  │  ▼ -5         │  │               │                │
│  └───────────────┘  └───────────────┘  └───────────────┘                │
│                                                                          │
│  RISK HEATMAP                                                            │
│  ┌────────┬────────┬────────┬────────┬────────┐                         │
│  │ PCI-DSS│  GDPR  │  RBI   │  CCPA  │  LGPD  │                         │
│  │   🔴   │   🟡   │   🟡   │   🟢   │   🟢   │                         │
│  │   12   │   8    │   3    │   0    │   0    │                         │
│  └────────┴────────┴────────┴────────┴────────┘                         │
│                                                                          │
│  RECENT ALERTS                                                           │
│  ─────────────────────────────────────────────────────────               │
│  🔴 09:14 | CRITICAL | Transaction anomaly - Merchant MID-4521          │
│  🔴 08:45 | CRITICAL | PAN detected in settlement log                   │
│  🟡 08:30 | HIGH     | Bank BNK-123 cert expires in 5 days              │
│                                                  [View All →]            │
│                                                                          │
│  AGENT STATUS                                                            │
│  ─────────────────────────────────────────────────────────               │
│  Agent 1 (Reg Intel)     ● Online | Last: 5 min ago                     │
│  Agent 3 (Transaction)   ● Online | 2.3M tx/hour                        │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

**Components to use (shadcn):**
- `Card` for metric boxes
- `Badge` for status indicators
- `Table` for alerts list
- Custom risk heatmap (simple div grid with colors)

---

### Screen 2: Alert Detail (P0 - MUST HAVE)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ← Back to Dashboard                                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  🔴 CRITICAL: PAN Detected in Transaction Log                           │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                          │
│  DETAILS                                                                 │
│  ─────────────────────────────────────────────────────────               │
│  Regulation:    PCI-DSS Requirement 3.4                                  │
│  Detected:      2026-01-05 09:14:23 UTC                                  │
│  Merchant:      MID-4521 (ElectroMart Inc)                               │
│  Status:        Open                                                     │
│                                                                          │
│  EVIDENCE                                                                │
│  ─────────────────────────────────────────────────────────               │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │ Log Entry:                                                           ││
│  │ 2026-01-05 09:14:22 | AUTH | 4532-XXXX-XXXX-9012 | $150.00          ││
│  │                                                                      ││
│  │ Issue: Full PAN visible (should be masked)                          ││
│  └─────────────────────────────────────────────────────────────────────┘│
│                                                                          │
│  RECOMMENDED ACTIONS                                                     │
│  ─────────────────────────────────────────────────────────               │
│  1. Notify merchant's acquiring bank                                    │
│  2. Request log sanitization within 24 hours                            │
│                                                                          │
│  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐               │
│  │ Create Case    │ │ Send Alert     │ │ Mark Resolved  │               │
│  └────────────────┘ └────────────────┘ └────────────────┘               │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

**Components:**
- `Card` for sections
- `Button` for actions
- `Badge` for severity
- Code block styling for evidence

---

### Screen 3: Chat Interface (P0 - MUST HAVE)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ASK AEGIS                                                   [← Back]   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │                                                                      ││
│  │  You: "Which banks have expiring certifications?"                   ││
│  │                                                                      ││
│  │  ────────────────────────────────────────────────────────────────── ││
│  │                                                                      ││
│  │  AEGIS:                                                              ││
│  │                                                                      ││
│  │  3 banks have PCI certifications expiring within 30 days:           ││
│  │                                                                      ││
│  │  | Bank ID   | Name           | Expires  | Risk   |                 ││
│  │  |-----------|----------------|----------|--------|                 ││
│  │  | BNK-1234  | First National | Jan 15   | 🔴 High |                ││
│  │  | BNK-5678  | Metro Credit   | Jan 22   | 🟡 Med  |                ││
│  │  | BNK-9012  | Pacific Trust  | Feb 1    | 🟡 Med  |                ││
│  │                                                                      ││
│  │  [Send Reminders] [View Details]                                    ││
│  │                                                                      ││
│  └─────────────────────────────────────────────────────────────────────┘│
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │  Type your question...                                     [Send]   ││
│  └─────────────────────────────────────────────────────────────────────┘│
│                                                                          │
│  Suggested: [What's our PCI risk?] [New regulations?]                   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

**Components:**
- `Input` for query
- `Button` for send
- `ScrollArea` for chat history
- Render markdown in responses (use `react-markdown`)

**IMPORTANT:** Response is **TEXT/MARKDOWN**, not dynamic UI components.

---

### Screen 4: Entity Table (P1 - SHOULD HAVE)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  MEMBER BANKS                                              [← Back]     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  [Search...                    ] [Status ▼] [Risk ▼] [Export]           │
│                                                                          │
│  ┌───────────┬────────────────┬────────────┬─────────┬─────────────────┐│
│  │ Bank ID   │ Name           │ PCI Status │ Risk    │ Action          ││
│  ├───────────┼────────────────┼────────────┼─────────┼─────────────────┤│
│  │ BNK-1234  │ First National │ ⚠️ 5 days  │ 🔴 High │ [View]          ││
│  │ BNK-5678  │ Metro Credit   │ ⚠️ 12 days │ 🟡 Med  │ [View]          ││
│  │ BNK-9012  │ Pacific Trust  │ ✅ Valid   │ 🟢 Low  │ [View]          ││
│  └───────────┴────────────────┴────────────┴─────────┴─────────────────┘│
│                                                                          │
│  Page 1 of 10                                      [←] [1] [2] [3] [→] │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

**Components:**
- `Table` from shadcn
- `Input` for search
- `Select` for filters
- `Pagination`

---

## 4. DESIGN SYSTEM

### Color Palette (Dark Theme - "Executive Command")

```css
--background: #0a0a0a;     /* Near black */
--card: #1a1a1a;           /* Dark gray */
--card-hover: #252525;     /* Slightly lighter */
--border: #333333;         /* Subtle borders */

--primary: #3b82f6;        /* Blue - primary actions */
--success: #16a34a;        /* Green - good status */
--warning: #f59e0b;        /* Amber - warnings */
--critical: #dc2626;       /* Red - critical */

--text-primary: #f8fafc;   /* White text */
--text-secondary: #94a3b8; /* Gray text */
```

### Typography
```css
--font-sans: 'Inter', sans-serif;
--font-mono: 'SF Mono', monospace;  /* For code/data */
```

### Status Indicators
```
🔴 Critical / High Risk  → red-500
🟡 Warning / Medium Risk → amber-500
🟢 Good / Low Risk       → green-500
● Online                 → green-500
○ Offline                → gray-500
```

---

## 5. DO's and DON'Ts

### ✅ DO

| Do This | Why |
|---------|-----|
| Use shadcn components | Pre-built, consistent |
| Keep state in components | Simple, no global state needed |
| Make mock data if API not ready | Demo must work |
| Use dark theme | Matches "Executive Command" design |
| Add loading states | Professional feel |
| Make buttons do something (even console.log) | Demo needs interactivity |

### ❌ DON'T

| Don't Do This | Why |
|---------------|-----|
| Build GenUI (AI-generated components) | Was explicitly dropped - see AGENT_COORDINATION.md |
| Add complex state management | Overkill for 4 screens |
| Over-engineer routing | Simple Next.js pages |
| Build custom chart library | Use simple colored divs |
| Polish pixel-perfect | Demo quality, not production |
| Add authentication | MVP skip |

---

## 6. API ENDPOINTS (What Backend Will Provide)

If backend not ready, **mock these responses**.

```typescript
// GET /api/dashboard/summary
interface DashboardSummary {
  compliance_score: number;      // 0-100
  score_change: number;          // +/- from yesterday
  open_violations: number;
  critical_alerts: number;
  agents: Agent[];
}

// GET /api/alerts
interface Alert {
  id: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  title: string;
  description: string;
  timestamp: string;
  entity_id?: string;
  regulation?: string;
  status: 'open' | 'investigating' | 'resolved';
}

// GET /api/alerts/{id}
interface AlertDetail extends Alert {
  evidence: string;              // Code/log snippet
  recommendations: string[];
  context: {
    similar_violations: number;
    entity_name: string;
    entity_volume: string;
  };
}

// POST /api/chat
interface ChatRequest {
  query: string;
}
interface ChatResponse {
  response: string;              // Markdown text
  suggested_actions?: string[];
}

// GET /api/entities
interface Entity {
  id: string;
  name: string;
  type: 'bank' | 'merchant' | 'vendor';
  pci_status: 'valid' | 'expiring' | 'expired';
  pci_expiry?: string;
  risk_level: 'high' | 'medium' | 'low';
  violation_count: number;
}

// GET /api/risk-heatmap
interface RiskHeatmap {
  regulations: {
    name: string;           // "PCI-DSS", "GDPR", etc.
    risk_level: 'high' | 'medium' | 'low';
    violation_count: number;
  }[];
}
```

---

## 7. MOCK DATA (Use If API Not Ready)

```typescript
// mockData.ts

export const mockDashboard = {
  compliance_score: 78,
  score_change: 3,
  open_violations: 23,
  critical_alerts: 3,
  agents: [
    { id: 1, name: "Regulatory Intelligence", status: "online", last_run: "5 min ago" },
    { id: 2, name: "Ecosystem Tracker", status: "online", last_run: "10 min ago" },
    { id: 3, name: "Transaction Monitor", status: "online", last_run: "now", stats: "2.3M tx/hour" },
    { id: 4, name: "Cross-Jurisdiction", status: "online", last_run: "1 hour ago" },
    { id: 5, name: "Evidence Engine", status: "online", last_run: "30 min ago" },
  ]
};

export const mockAlerts = [
  {
    id: "ALT-001",
    severity: "critical",
    title: "Transaction anomaly detected",
    description: "Unusual volume spike from Merchant MID-4521",
    timestamp: "2026-01-05T09:14:00Z",
    entity_id: "MID-4521",
    regulation: "PCI-DSS",
    status: "open"
  },
  {
    id: "ALT-002",
    severity: "critical",
    title: "PAN detected in settlement log",
    description: "Full card number found in plaintext",
    timestamp: "2026-01-05T08:45:00Z",
    entity_id: "MID-4521",
    regulation: "PCI-DSS 3.4",
    status: "open"
  },
  {
    id: "ALT-003",
    severity: "high",
    title: "Bank certification expiring",
    description: "BNK-123 PCI certification expires in 5 days",
    timestamp: "2026-01-05T08:30:00Z",
    entity_id: "BNK-123",
    regulation: "PCI-DSS",
    status: "open"
  }
];

export const mockRiskHeatmap = [
  { name: "PCI-DSS", risk_level: "high", violation_count: 12 },
  { name: "GDPR", risk_level: "medium", violation_count: 8 },
  { name: "RBI", risk_level: "medium", violation_count: 3 },
  { name: "CCPA", risk_level: "low", violation_count: 0 },
  { name: "LGPD", risk_level: "low", violation_count: 0 },
];

export const mockEntities = [
  { id: "BNK-1234", name: "First National Bank", type: "bank", pci_status: "expiring", pci_expiry: "2026-01-15", risk_level: "high", violation_count: 3 },
  { id: "BNK-5678", name: "Metro Credit Union", type: "bank", pci_status: "expiring", pci_expiry: "2026-01-22", risk_level: "medium", violation_count: 1 },
  { id: "BNK-9012", name: "Pacific Trust", type: "bank", pci_status: "valid", pci_expiry: "2026-06-30", risk_level: "low", violation_count: 0 },
  { id: "MID-4521", name: "ElectroMart Inc", type: "merchant", pci_status: "valid", pci_expiry: "2026-03-15", risk_level: "high", violation_count: 5 },
];

export const mockChatResponse = (query: string) => ({
  response: `Based on your query "${query}", here's what I found:\n\n**Summary:** This is a mock response demonstrating the chat interface.\n\nIn production, this would be generated by the LLM based on vector search results and live data.`,
  suggested_actions: ["View Details", "Generate Report"]
});
```

---

## 8. PROJECT STRUCTURE

```
frontend/
├── app/
│   ├── layout.tsx           # Root layout (dark theme)
│   ├── page.tsx             # Dashboard
│   ├── alerts/
│   │   ├── page.tsx         # Alert list
│   │   └── [id]/page.tsx    # Alert detail
│   ├── chat/
│   │   └── page.tsx         # Chat interface
│   └── entities/
│       └── page.tsx         # Entity table
├── components/
│   ├── ui/                  # shadcn components
│   ├── dashboard/
│   │   ├── MetricCard.tsx
│   │   ├── RiskHeatmap.tsx
│   │   ├── AlertList.tsx
│   │   └── AgentStatus.tsx
│   ├── chat/
│   │   ├── ChatMessage.tsx
│   │   └── ChatInput.tsx
│   └── layout/
│       ├── Header.tsx
│       └── Sidebar.tsx
├── lib/
│   ├── api.ts               # API client
│   └── mockData.ts          # Mock data
└── styles/
    └── globals.css          # Tailwind + custom
```

---

## 9. SESSION LOGGING (Please Fill This)

After your implementation session, update this:

```markdown
## UI Agent Session Log

### Session 1
Date: ___
Duration: ___

#### Context Documents Used
- [ ] UI_CONTEXT.md - Helpful: ___
- [ ] ARCHITECTURE.md - Used sections: ___
- [ ] AGENT_COORDINATION.md - Referenced: ___

#### What Was Helpful
- ___

#### What Was Missing
- ___

#### Decisions Made
- ___

#### Work Completed
- [ ] Dashboard
- [ ] Alert Detail
- [ ] Chat
- [ ] Entity Table

#### Issues/Blockers
- ___

#### Handoff Notes
- ___
```

---

## 10. QUESTIONS? ASK MUDASSIR

If something is unclear:
1. Check `AGENT_COORDINATION.md` for context
2. Check `ARCHITECTURE.md` for technical details
3. If still unclear, ask in chat

---

*Last Updated: 2026-01-05 01:00 IST*
*For: UI Implementation Agent*
