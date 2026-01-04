# AEGIS - Technical Architecture Document
## Visa Hackathon PS4: Agentic AI Compliance Platform
### Version 2.0 (Visa-Specific Design)

---

## 1. EXECUTIVE SUMMARY

### What is AEGIS?

AEGIS (Autonomous Enterprise Governance & Intelligence System) is an agentic AI platform that provides continuous PCI/PII compliance for financial services organizations. It uses autonomous agents that can:

- Make decisions without constant human supervision
- Plan and break down complex compliance tasks
- Access multiple data sources
- Adapt based on regulatory changes and feedback

### Target User: Visa's Perspective

AEGIS is designed for a **payment network operator** like Visa that:
- Operates in 200+ countries
- Works with 15,000+ member banks
- Processes billions of daily transactions
- Must comply with PCI-DSS (which they created) + global regulations
- Manages merchant/member compliance across their ecosystem

---

## 2. PROBLEM ANALYSIS

### The Core Problem

```
Financial services operate in a DYNAMIC regulatory environment:

• 100+ regulations across jurisdictions
• Regulations change ~40 times/year
• 80% of violations found AFTER damage (during audits)
• $270 billion spent annually on compliance globally
• Average breach takes 279 days to detect

Traditional compliance is:
MANUAL → REACTIVE → SILOED → SLOW

AEGIS makes it:
AUTOMATED → PROACTIVE → UNIFIED → REAL-TIME
```

### Visa's Specific Pain Points

| Pain Point | Current State | AEGIS Solution |
|------------|---------------|----------------|
| Regulatory changes across 200+ countries | Legal teams manually track | Agent 1 auto-monitors |
| Member bank compliance tracking | Periodic audits, self-attestation | Agent 2 continuous tracking |
| Transaction pattern anomalies | Batch analysis, slow detection | Agent 3 real-time detection |
| Cross-border data flow compliance | Manual jurisdiction mapping | Agent 4 auto-analysis |
| Audit report generation | Weeks of manual compilation | Agent 5 instant generation |
| Natural language compliance queries | Ask legal team, wait days | GenUI instant answer |

---

## 3. DATA SOURCES (VISA-SPECIFIC)

### External Sources (Regulatory Intelligence)

| Source Category | Examples | Monitoring Frequency | Method |
|-----------------|----------|---------------------|--------|
| **Government Regulators** | europa.eu (GDPR), RBI, FTC, MAS, FCA | Daily | Web scraping + RSS |
| **Standards Bodies** | PCI Security Standards Council, ISO, NIST | Weekly | API + Web scraping |
| **Legal Intelligence** | Enforcement actions, court decisions | Daily | Feed subscription |
| **Industry Publications** | Regulatory proposals, guidance docs | Weekly | RSS + email parsing |

### Internal Sources (Visa Ecosystem)

| Source | Data Contents | Compliance Use |
|--------|---------------|----------------|
| **Transaction Logs** | Authorization requests, settlements, chargebacks | Pattern anomaly detection, breach indicators |
| **Member Bank Records** | Certification dates, compliance status, audit history | Ecosystem compliance tracking |
| **Merchant Database** | PCI status, SAQ submissions, QSA reports | Merchant compliance management |
| **Cross-Border Flow Data** | Transaction routes, data locations | Data localization compliance |
| **Third-Party Vendor Registry** | Service provider certifications, risk ratings | Third-party risk management |
| **Incident Database** | Breach notifications, compromise events | Risk tracking and patterns |
| **Regulatory Filing Records** | Submitted reports, regulatory correspondence | Audit trail and evidence |

### What We DON'T Monitor (Clarification)

| NOT Monitored | Reason |
|---------------|--------|
| Internal code repositories | Visa doesn't audit member bank source code |
| Slack/Teams messages | Not Visa's scope |
| Member bank CRM systems | Outside Visa's visibility |
| Developer environments | Not relevant to payment network compliance |

---

## 4. AGENT ARCHITECTURE

### Agent Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AEGIS AGENT ARCHITECTURE                             │
│                           (5 Specialized Agents)                             │
└─────────────────────────────────────────────────────────────────────────────┘

    EXTERNAL WORLD                           VISA ECOSYSTEM
    ─────────────────                        ─────────────────
    │ Regulatory    │                        │ Transaction   │
    │ Sources       │                        │ Data          │
    └───────┬───────┘                        └───────┬───────┘
            │                                        │
            ▼                                        ▼
    ┌───────────────────────────────────────────────────────────────────────┐
    │                           AGENT LAYER                                  │
    │                                                                        │
    │   ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐  │
    │   │ AGENT 1         │    │ AGENT 2         │    │ AGENT 3         │  │
    │   │ Regulatory      │    │ Ecosystem       │    │ Transaction     │  │
    │   │ Intelligence    │    │ Compliance      │    │ Monitor         │  │
    │   │                 │    │ Tracker         │    │                 │  │
    │   │ Monitors:       │    │ Tracks:         │    │ Monitors:       │  │
    │   │ • Govt websites │    │ • Member banks  │    │ • Auth requests │  │
    │   │ • Standards     │    │ • Merchants     │    │ • Settlements   │  │
    │   │ • Legal feeds   │    │ • Vendors       │    │ • Data flows    │  │
    │   └────────┬────────┘    └────────┬────────┘    └────────┬────────┘  │
    │            │                      │                      │            │
    │            └──────────────────────┼──────────────────────┘            │
    │                                   │                                    │
    │                                   ▼                                    │
    │                       ┌───────────────────────┐                        │
    │                       │     SHARED MEMORY      │                        │
    │                       │ ─────────────────────  │                        │
    │                       │ • Vector DB (pgvector) │                        │
    │                       │ • Event Bus            │                        │
    │                       │ • Context Store        │                        │
    │                       │ • Feedback Patterns    │                        │
    │                       └───────────┬───────────┘                        │
    │                                   │                                    │
    │            ┌──────────────────────┼──────────────────────┐            │
    │            │                      │                      │            │
    │   ┌────────▼────────┐    ┌────────▼────────┐            │            │
    │   │ AGENT 4         │    │ AGENT 5         │            │            │
    │   │ Cross-          │    │ Evidence &      │            │            │
    │   │ Jurisdiction    │    │ Reporting       │            │            │
    │   │ Analyzer        │    │ Engine          │            │            │
    │   │                 │    │                 │            │            │
    │   │ Analyzes:       │    │ Generates:      │            │            │
    │   │ • Data routes   │    │ • Audit reports │            │            │
    │   │ • Reg conflicts │    │ • Evidence pkgs │            │            │
    │   │ • Systemic risk │    │ • GRC cases     │            │            │
    │   └─────────────────┘    └─────────────────┘            │            │
    │                                                          │            │
    └──────────────────────────────────────────────────────────┼────────────┘
                                                               │
                                                               ▼
                                                       USER INTERFACE
                                                       • Dashboard
                                                       • GenUI Chat
                                                       • Reports
```

---

### Agent 1: Regulatory Intelligence

**Purpose:** Monitor regulatory landscape and interpret changes

---

#### SECURITY DESIGN: Admin-Controlled Sources

> ⚠️ **SECURITY CONSIDERATION:** Agent 1 does NOT auto-discover URLs.
> All regulatory sources are admin-controlled via database table.
> This prevents **prompt injection attacks** via malicious URLs.

**Sources Table (PostgreSQL):**
```sql
CREATE TABLE regulatory_sources (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            VARCHAR(255) NOT NULL,
    url             TEXT NOT NULL,
    region          VARCHAR(50) NOT NULL,  -- 'EU', 'US', 'IN', 'GLOBAL'
    sector          VARCHAR(50) NOT NULL,  -- 'BANKING', 'PAYMENTS', 'INSURANCE'
    source_type     VARCHAR(50) NOT NULL,  -- 'GOV_REGULATOR', 'STANDARDS_BODY', 'LEGAL_INTEL'
    fetch_method    VARCHAR(50) NOT NULL,  -- 'SCRAPE', 'RSS', 'API', 'EMAIL'
    frequency       VARCHAR(20) NOT NULL,  -- 'DAILY', 'WEEKLY', 'MONTHLY'
    is_active       BOOLEAN DEFAULT true,
    last_fetched    TIMESTAMP,
    last_hash       TEXT,                   -- For change detection
    created_by      VARCHAR(100) NOT NULL,  -- Admin who added
    created_at      TIMESTAMP DEFAULT NOW(),
    expires_at      TIMESTAMP,              -- NULL = no expiry
    notes           TEXT
);
```

**Example Source Entries:**
| Name | URL | Region | Sector | Method | Frequency |
|------|-----|--------|--------|--------|-----------|
| EU GDPR Portal | europa.eu/gdpr | EU | BANKING | SCRAPE | DAILY |
| RBI Notifications | rbi.org.in/Scripts/NotificationUser.aspx | IN | BANKING | SCRAPE | DAILY |
| PCI SSC Updates | pcisecuritystandards.org/updates | GLOBAL | PAYMENTS | RSS | WEEKLY |
| FTC Enforcement | ftc.gov/enforcement | US | BANKING | SCRAPE | DAILY |
| NIST Frameworks | nvd.nist.gov | US | BANKING | API | WEEKLY |

**Admin Interface:**
- Only users with `ADMIN` role can add/edit/delete sources
- URL validation required (must be https, known domain patterns)
- Audit log of all source changes

> 🔒 **TODO (Security Assessment):** 
> - Implement URL allowlist validation
> - Sandbox scraping in isolated container
> - Rate limit per source to prevent abuse
> - Content sanitization before LLM processing

---

#### Function Flows

**Flow 1: Scheduled Source Fetch**
```
┌───────────────────────────────────────────────────────────────────────────┐
│ FLOW: SCHEDULED_FETCH                                                      │
│ Trigger: CRON (based on source.frequency)                                  │
│ Purpose: Check for regulatory updates                                       │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  1. SCHEDULER queries active sources due for fetch                         │
│     │                                                                      │
│     ▼                                                                      │
│  2. For each source:                                                       │
│     ├── fetch_source(source.url, source.fetch_method)                      │
│     │   └── Returns: raw_content, content_hash                             │
│     │                                                                      │
│  3. Compare content_hash with source.last_hash                             │
│     │                                                                      │
│     ├── IF SAME → Update last_fetched, skip processing                     │
│     │                                                                      │
│     └── IF DIFFERENT → Continue to step 4                                  │
│                                                                            │
│  4. parse_regulatory_content(raw_content)                                  │
│     │   └── LLM: Extract structured obligations                            │
│     │   └── Returns: {title, summary, obligations[], effective_date}       │
│     │                                                                      │
│  5. diff_with_previous(regulation_id)                                      │
│     │   └── Compare with stored version                                    │
│     │   └── Returns: {added[], removed[], modified[]}                      │
│     │                                                                      │
│  6. IF changes exist:                                                      │
│     ├── store_regulation(parsed_content) → PostgreSQL                      │
│     ├── embed_regulation(parsed_content) → pgvector                        │
│     ├── calculate_impact(parsed_content) → affected member banks           │
│     ├── publish_event("new_regulation_detected") → Event Bus               │
│     └── create_alert(type="REGULATION_UPDATE", severity=calculated)        │
│                                                                            │
│  7. Update source.last_fetched, source.last_hash                           │
│                                                                            │
└───────────────────────────────────────────────────────────────────────────┘
```

**Flow 2: On-Demand Regulation Search**
```
┌───────────────────────────────────────────────────────────────────────────┐
│ FLOW: REGULATION_SEARCH                                                    │
│ Trigger: User query via chat or API                                        │
│ Purpose: Find relevant regulations for a query                              │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  1. User query: "What regulations apply to cross-border payments in EU?"   │
│     │                                                                      │
│     ▼                                                                      │
│  2. semantic_search(query, filters={region: "EU"})                         │
│     │   └── Vector similarity search in pgvector                           │
│     │   └── Returns: [regulation_ids] ranked by relevance                  │
│     │                                                                      │
│  3. fetch_full_regulations(regulation_ids)                                 │
│     │   └── Get full text + obligations from PostgreSQL                    │
│     │                                                                      │
│  4. synthesize_answer(query, regulations)                                  │
│     │   └── LLM: Generate natural language response                        │
│     │   └── Include: citations, obligation summaries, due dates            │
│     │                                                                      │
│  5. Return formatted response to user                                      │
│                                                                            │
└───────────────────────────────────────────────────────────────────────────┘
```

**Flow 3: Impact Analysis**
```
┌───────────────────────────────────────────────────────────────────────────┐
│ FLOW: IMPACT_ANALYSIS                                                      │
│ Trigger: New regulation detected OR user request                           │
│ Purpose: Determine which entities are affected                              │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  1. New regulation detected with scope: {region: "IN", sector: "PAYMENTS"} │
│     │                                                                      │
│     ▼                                                                      │
│  2. query_affected_entities(region, sector)                                │
│     │   └── Filter entities by jurisdiction                                │
│     │   └── Returns: [member_bank_ids, merchant_ids]                       │
│     │                                                                      │
│  3. For each affected entity:                                              │
│     ├── check_current_compliance(entity, regulation)                       │
│     │   └── Compare entity's current controls vs new requirements          │
│     │                                                                      │
│  4. calculate_gap_severity(entity, gaps)                                   │
│     │   └── Score: (impact × urgency × complexity)                         │
│     │                                                                      │
│  5. generate_impact_report()                                               │
│     │   └── {affected_count, gap_summary, timeline, recommendations}       │
│     │                                                                      │
│  6. Store in findings table, notify relevant relationship managers         │
│                                                                            │
└───────────────────────────────────────────────────────────────────────────┘
```

---

#### Tools (Updated)

```python
class RegulatoryIntelligenceAgent:
    tools = [
        # Source Management (read-only for agent, admin writes via UI)
        "list_active_sources(filters) → sources[]",
        
        # Fetching
        "fetch_source(source_id) → {raw_content, hash, timestamp}",
        
        # Parsing
        "parse_regulatory_content(content) → StructuredRegulation",
        "diff_with_previous(regulation_id) → RegulationDiff",
        
        # Storage
        "store_regulation(regulation) → regulation_id",
        "embed_regulation(regulation) → embedding_id",
        
        # Analysis
        "semantic_search(query, filters) → [regulation_ids]",
        "calculate_impact(regulation_id) → ImpactReport",
        
        # Events
        "publish_event(event_type, payload) → confirmation",
    ]
```

---

#### Data Structures

```python
from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class StructuredObligation(BaseModel):
    id: str
    text: str
    category: str  # "DATA_PROTECTION", "DISCLOSURE", "RETENTION", etc.
    applies_to: List[str]  # ["banks", "merchants", "processors"]
    effective_date: Optional[date]
    penalty_reference: Optional[str]

class StructuredRegulation(BaseModel):
    id: str
    title: str
    source_url: str
    region: str
    sector: str
    summary: str
    obligations: List[StructuredObligation]
    effective_date: Optional[date]
    compliance_deadline: Optional[date]
    version: str
    fetched_at: datetime
    
class RegulationDiff(BaseModel):
    regulation_id: str
    previous_version: str
    current_version: str
    added_obligations: List[str]
    removed_obligations: List[str]
    modified_obligations: List[dict]
    significance: str  # "MAJOR", "MINOR", "CLARIFICATION"

class ImpactReport(BaseModel):
    regulation_id: str
    affected_entities: List[str]
    affected_count: int
    gap_summary: str
    estimated_effort: str  # "LOW", "MEDIUM", "HIGH"
    compliance_deadline: Optional[date]
    recommendations: List[str]
```

**Frequency:** Daily for major sources, weekly for stable sources

---

### Agent 2: Ecosystem Compliance Tracker

**Purpose:** Track compliance status of member banks, merchants, vendors

**Inputs:**
- Member bank compliance database
- Merchant PCI certification records
- Service provider assessment status
- Historical audit data

**Outputs:**
- Real-time compliance status by entity
- Expiring certification alerts
- Risk-ranked entity list
- Remediation recommendations

**Tools:**
```python
class EcosystemComplianceAgent:
    tools = [
        "query_member_status(member_id) → compliance_record",
        "list_expiring_certifications(days) → entities[]",
        "calculate_entity_risk(entity_id) → risk_score",
        "generate_compliance_reminder(entity_id) → notification",
        "update_compliance_status(entity_id, status) → confirmation",
    ]
```

**Detection Method:** Rule engine + SQL queries

**Frequency:** Real-time on status changes, daily batch reconciliation

---

### Agent 3: Transaction Compliance Monitor

**Purpose:** Monitor transaction patterns for compliance signals

**Inputs:**
- Transaction authorization logs
- Settlement records
- Cross-border payment flows
- Chargeback patterns

**Outputs:**
- Anomaly alerts (potential breaches)
- Data flow compliance status
- Breach indicator patterns
- Geographic compliance mapping

**What It Detects:**

| Pattern | Indication | Urgency |
|---------|------------|---------|
| Full PAN in unexpected fields | PCI violation | Critical |
| Unusual transaction volume from merchant | Potential breach | High |
| Data routing through non-compliant regions | Localization violation | High |
| Spike in chargebacks | Potential compromise | Medium |
| Settlement timing anomalies | Process violation | Medium |

**Tools:**
```python
class TransactionMonitorAgent:
    tools = [
        "scan_transaction_batch(batch_id) → violations[]",
        "check_data_route(transaction) → compliance_status",
        "detect_pattern_anomaly(merchant_id) → anomaly_report",
        "flag_breach_indicator(pattern) → alert",
        "get_merchant_baseline(merchant_id) → expected_patterns",
    ]
```

**Detection Method:** 
- Layer 1: Regex for PAN patterns + Luhn validation
- Layer 2: Statistical baseline comparison (anomaly)
- Layer 3: LLM for complex pattern interpretation

**Frequency:** Real-time streaming

---

### Agent 4: Cross-Jurisdiction Analyzer

**Purpose:** Analyze compliance across multiple regulatory domains

**Inputs:**
- Transaction geography data
- Regulatory requirements by region
- Data flow routing information
- Obligation database (from Agent 1)

**Outputs:**
- Per-transaction jurisdiction assessment
- Conflicting regulation alerts
- Systemic risk identification
- Cross-border compliance guidance

**Example Analysis:**
```
Transaction: Card issued in Germany (GDPR), 
            processed in Singapore (PDPA), 
            settled in US (CCPA)

Agent 4 Output:
{
  "jurisdictions": ["EU-GDPR", "SG-PDPA", "US-CCPA"],
  "applicable_rules": [
    "GDPR Art 44-49: Cross-border transfer requirements",
    "PDPA: Data processing obligations",
    "CCPA: Consumer rights notification"
  ],
  "compliance_status": "COMPLIANT",
  "conditions": "Standard Contractual Clauses must be in place",
  "risks": ["GDPR adequacy decision may change post-Schrems II"]
}
```

**Tools:**
```python
class CrossJurisdictionAgent:
    tools = [
        "map_jurisdictions(transaction) → regions[]",
        "lookup_regulations(region) → obligations[]",
        "check_conflicts(obligations[]) → conflicts[]",
        "assess_data_flow_compliance(route) → status",
        "generate_guidance(transaction) → recommendations",
    ]
```

**Detection Method:** Rule engine + semantic search + LLM reasoning

**Frequency:** On-demand per transaction batch

---

### Agent 5: Evidence & Reporting Engine

**Purpose:** Generate audit-ready outputs and manage remediation

**Inputs:**
- All other agent outputs
- Historical compliance data
- Audit requirements by framework

**Outputs:**
- Audit evidence packages (PDF)
- Regulatory reports (GDPR Art 30, PCI AOC, etc.)
- Risk dashboards
- GRC workflow cases
- Remediation tracking

**Tools:**
```python
class EvidenceReportingAgent:
    tools = [
        "compile_evidence_package(scope, timeframe) → package",
        "generate_regulatory_report(framework, region) → report",
        "create_grc_case(issue, priority) → case_id",
        "update_remediation_status(case_id, status) → confirmation",
        "export_pdf(document) → file_path",
        "send_to_stakeholder(document, recipient) → delivery_status",
    ]
```

**Detection Method:** Template engine + LLM for narrative generation

**Frequency:** On-demand + scheduled (monthly reports)

---

## 5. SHARED MEMORY ARCHITECTURE

### Purpose

Enable **context coherence** across agents - when one agent finds something, others can use that knowledge immediately.

### Components

```
SHARED MEMORY LAYER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────────┐
│ 1. VECTOR DATABASE (pgvector in PostgreSQL)            │
│                                                         │
│ Stores:                                                 │
│ • Regulation text embeddings                           │
│ • Policy document embeddings                           │
│ • Historical finding embeddings                        │
│                                                         │
│ Enables:                                               │
│ • Semantic search ("Find regulations about consent")   │
│ • Similar case lookup                                  │
│ • Cross-reference detection                            │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 2. EVENT BUS (Redis or PostgreSQL LISTEN/NOTIFY)       │
│                                                         │
│ Events:                                                 │
│ • "new_regulation_detected" → triggers policy mapping  │
│ • "violation_found" → triggers risk scoring            │
│ • "certification_expired" → triggers alert             │
│                                                         │
│ Enables:                                               │
│ • Real-time agent coordination                         │
│ • Event-driven workflows                               │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 3. CONTEXT STORE (PostgreSQL tables)                   │
│                                                         │
│ Tables:                                                 │
│ • regulations (id, text, jurisdiction, embedding)      │
│ • obligations (id, regulation_id, description, status) │
│ • entities (id, type, compliance_status, risk_score)   │
│ • findings (id, agent, type, details, timestamp)       │
│ • remediation (id, finding_id, status, assignee)       │
│                                                         │
│ Enables:                                               │
│ • Persistent state across agent runs                   │
│ • Audit trail                                          │
│ • Historical analysis                                  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 4. FEEDBACK PATTERNS (Learning from decisions)         │
│                                                         │
│ When human reviews agent output:                       │
│ • [Approve] → Strengthen pattern weight                │
│ • [Reject] → Reduce pattern weight                     │
│ • [False Positive] → Add to exceptions                 │
│                                                         │
│ Enables:                                               │
│ • Adaptive behavior over time                          │
│ • Reduced false positives                              │
│ • Organization-specific tuning                         │
└─────────────────────────────────────────────────────────┘
```

---

## 6. DETECTION METHODS BY USE CASE

### Method Selection Matrix

| Use Case | Layer 1 (Regex) | Layer 2 (Semantic) | Layer 3 (LLM) |
|----------|-----------------|-------------------|---------------|
| PAN in transaction data | ✅ Primary | - | - |
| Regulation change detection | - | ✅ Diff + similarity | ✅ Interpretation |
| Policy gap analysis | - | ✅ Similarity search | ✅ Reasoning |
| Member compliance status | - | - | Rule engine |
| Transaction anomaly | ✅ Baseline check | - | ✅ Complex patterns |
| Cross-jurisdiction mapping | - | ✅ Regulation lookup | ✅ Conflict analysis |
| Report generation | - | - | ✅ Narrative |
| Natural language queries | - | ✅ Context retrieval | ✅ Response |

### Why Hybrid Approach?

```
COST vs ACCURACY vs SPEED

Layer 1 (Regex/Rules):
├── Speed: <1ms
├── Cost: $0
├── Accuracy: 100% for defined patterns
└── Use: Known patterns, high volume data

Layer 2 (Semantic/Embeddings):
├── Speed: 10-50ms
├── Cost: Low (embedding once)
├── Accuracy: ~95% with good training
└── Use: Similarity, context, search

Layer 3 (LLM - Gemini):
├── Speed: 100-500ms
├── Cost: Higher (per call)
├── Accuracy: Context-dependent
└── Use: Reasoning, interpretation, generation

STRATEGY: Use cheapest/fastest method that works for each task
```

### COMPLETE CHANNEL × METHOD × FREQUENCY MATRIX

```
┌────────────────────────────┬─────────────────────┬──────────────────┬─────────────────────────────────────────┐
│ CHANNEL                    │ DETECTION METHOD    │ FREQUENCY        │ RATIONALE                               │
├────────────────────────────┼─────────────────────┼──────────────────┼─────────────────────────────────────────┤
│                            │                     │                  │                                         │
│ EXTERNAL REGULATORY SOURCES                                                                                   │
│ ────────────────────────────────────────────────────────────────────────────────────────────────────────────  │
│                            │                     │                  │                                         │
│ Government Regulators      │ Web scraping +      │ DAILY            │ High impact, frequent updates           │
│ (europa.eu, RBI, FTC)      │ LLM interpretation  │                  │ New rules can be critical               │
│                            │                     │                  │                                         │
│ Standards Bodies           │ API/RSS +           │ WEEKLY           │ Slower change cycles                    │
│ (PCI Council, NIST, ISO)   │ Diff detection      │                  │ Version updates predictable             │
│                            │                     │                  │                                         │
│ Enforcement Actions        │ Feed subscription + │ DAILY            │ Learn from others' fines                │
│ (Fines, penalties)         │ LLM summarization   │                  │ Early warning signals                   │
│                            │                     │                  │                                         │
│ Draft Proposals            │ RSS + Semantic      │ WEEKLY           │ Long-term planning only                 │
│ (Upcoming regulations)     │ similarity          │                  │ Not immediately actionable              │
│                            │                     │                  │                                         │
├────────────────────────────┼─────────────────────┼──────────────────┼─────────────────────────────────────────┤
│                            │                     │                  │                                         │
│ INTERNAL ECOSYSTEM DATA                                                                                       │
│ ────────────────────────────────────────────────────────────────────────────────────────────────────────────  │
│                            │                     │                  │                                         │
│ Transaction Authorization  │ REGEX (PAN) +       │ REAL-TIME        │ High volume, need speed                 │
│ Logs                       │ Luhn validation     │ (streaming)      │ Critical for breach detection           │
│                            │                     │                  │                                         │
│ Transaction Anomalies      │ Statistical         │ REAL-TIME        │ Baseline deviation = breach signal      │
│ (Volume, patterns)         │ baseline + LLM      │ (per batch)      │                                         │
│                            │                     │                  │                                         │
│ Settlement Records         │ Rule engine         │ HOURLY BATCH     │ Less time-critical than auth            │
│                            │                     │                  │                                         │
│ Cross-Border Data Flows    │ Rule lookup +       │ REAL-TIME        │ Route compliance is immediate           │
│                            │ Jurisdiction map    │ (per transaction)│                                         │
│                            │                     │                  │                                         │
│ Member Bank Status         │ SQL queries +       │ DAILY BATCH +    │ Status changes infrequent               │
│ (Certifications)           │ Rule engine         │ ON-CHANGE events │ Event-driven for updates                │
│                            │                     │                  │                                         │
│ Merchant PCI Status        │ SQL queries +       │ DAILY BATCH      │ Similar to member banks                 │
│ (SAQ, QSA reports)         │ Expiration rules    │                  │                                         │
│                            │                     │                  │                                         │
│ Third-Party Vendors        │ SQL queries +       │ WEEKLY           │ Vendor status changes slowly            │
│                            │ Risk scoring        │                  │                                         │
│                            │                     │                  │                                         │
│ Incident Reports           │ Event-driven +      │ REAL-TIME        │ Breaches need immediate response        │
│ (Breach notifications)     │ LLM analysis        │ (on submission)  │                                         │
│                            │                     │                  │                                         │
│ Chargeback Patterns        │ Statistical +       │ HOURLY           │ Leading indicator of compromise         │
│                            │ Threshold alerts    │                  │                                         │
│                            │                     │                  │                                         │
├────────────────────────────┼─────────────────────┼──────────────────┼─────────────────────────────────────────┤
│                            │                     │                  │                                         │
│ GENERATED OUTPUTS                                                                                             │
│ ────────────────────────────────────────────────────────────────────────────────────────────────────────────  │
│                            │                     │                  │                                         │
│ Policy Gap Analysis        │ Semantic search +   │ ON-DEMAND +      │ Triggered by new regulation             │
│                            │ LLM reasoning       │ ON NEW REG       │                                         │
│                            │                     │                  │                                         │
│ Compliance Reports         │ Template + LLM      │ MONTHLY +        │ Scheduled + on-demand                   │
│                            │ narrative           │ ON-DEMAND        │                                         │
│                            │                     │                  │                                         │
│ Risk Dashboards            │ Aggregation +       │ REAL-TIME        │ Always current                          │
│                            │ Visualization       │ (cached 1 min)   │                                         │
│                            │                     │                  │                                         │
│ Natural Language Queries   │ RAG + LLM           │ ON-DEMAND        │ User-initiated                          │
│                            │                     │                  │                                         │
└────────────────────────────┴─────────────────────┴──────────────────┴─────────────────────────────────────────┘
```

### Frequency Summary

| Frequency | Channels | Count |
|-----------|----------|-------|
| **REAL-TIME (streaming)** | Transaction auth, cross-border routes, incidents, dashboards | 4 |
| **HOURLY** | Settlements, chargebacks | 2 |
| **DAILY** | Govt regulators, enforcement, member/merchant status | 4 |
| **WEEKLY** | Standards bodies, proposals, vendors | 3 |
| **MONTHLY** | Scheduled compliance reports | 1 |
| **ON-DEMAND** | NL queries, reports, policy gaps | 3 |

---

## 7. USER INTERFACE

### Dashboard

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AEGIS COMMAND CENTER                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐ │
│  │ COMPLIANCE    │  │ MEMBER BANKS  │  │ VIOLATIONS    │  │ AGENTS        │ │
│  │ SCORE         │  │ AT RISK       │  │ (24h)         │  │ STATUS        │ │
│  │               │  │               │  │               │  │               │ │
│  │     78%       │  │      12       │  │      47       │  │     5/5       │ │
│  │    ▲ +3%      │  │    ▼ -2       │  │    ▲ +8       │  │   ● Online    │ │
│  └───────────────┘  └───────────────┘  └───────────────┘  └───────────────┘ │
│                                                                              │
│  REGULATION RISK HEATMAP                                                     │
│  ┌────────┬────────┬────────┬────────┬────────┐                             │
│  │ PCI-DSS│  GDPR  │  CCPA  │  RBI   │  LGPD  │                             │
│  │   🔴   │   🟡   │   🟢   │   🟡   │   🟢   │                             │
│  │  High  │  Med   │  Low   │  Med   │  Low   │                             │
│  └────────┴────────┴────────┴────────┴────────┘                             │
│                                                                              │
│  RECENT ALERTS                                                               │
│  ─────────────────────────────────────────────────────────────────          │
│  🔴 2 min ago  | Transaction anomaly detected at Merchant MID-4521          │
│  🟡 15 min ago | GDPR amendment published - impact analysis pending          │
│  🟢 1 hour ago | Bank BNK-789 certification renewed                          │
│                                                                              │
│  AGENT ACTIVITY                                                              │
│  ─────────────────────────────────────────────────────────────────          │
│  Agent 1: Last scan 5 min ago | 2 new regulations detected                  │
│  Agent 3: Monitoring 2.3M transactions/hour | 4 anomalies flagged           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### GenUI Chat Interface

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              ASK AEGIS                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  USER: "Which member banks have PCI certifications expiring in 30 days?"    │
│                                                                              │
│  ╔═══════════════════════════════════════════════════════════════════════╗  │
│  ║ AEGIS RESPONSE (GenUI - Dynamically Generated)                        ║  │
│  ║                                                                        ║  │
│  ║  📊 PCI Certifications Expiring Within 30 Days                         ║  │
│  ║                                                                        ║  │
│  ║  Bank ID      │ Name           │ Expires    │ Risk Level              ║  │
│  ║  ─────────────┼────────────────┼────────────┼──────────               ║  │
│  ║  BNK-1234     │ First National │ Jan 15     │ 🔴 High                 ║  │
│  ║  BNK-5678     │ Metro Credit   │ Jan 22     │ 🟡 Medium               ║  │
│  ║  BNK-9012     │ Pacific Trust  │ Feb 1      │ 🟡 Medium               ║  │
│  ║                                                                        ║  │
│  ║  Total: 3 banks | Average Transaction Volume: $2.3B/day               ║  │
│  ║                                                                        ║  │
│  ║  [Send Reminders] [View Details] [Generate Report]                    ║  │
│  ╚═══════════════════════════════════════════════════════════════════════╝  │
│                                                                              │
│  USER: "What's our compliance exposure if India mandates full data          │
│         localization?"                                                       │
│                                                                              │
│  ╔═══════════════════════════════════════════════════════════════════════╗  │
│  ║ AEGIS RESPONSE (Complex Analysis)                                     ║  │
│  ║                                                                        ║  │
│  ║  📈 India Data Localization Impact Analysis                            ║  │
│  ║                                                                        ║  │
│  ║  Current State:                                                        ║  │
│  ║  • 847M transactions/year originating from India                      ║  │
│  ║  • 23% currently processed via Singapore hub                          ║  │
│  ║  • 12 member banks affected                                           ║  │
│  ║                                                                        ║  │
│  ║  If full localization mandated:                                        ║  │
│  ║  • Estimated infrastructure cost: $45-60M                             ║  │
│  ║  • Timeline to compliance: 12-18 months                               ║  │
│  ║  • Revenue at risk: $120M/year during transition                      ║  │
│  ║                                                                        ║  │
│  ║  Recommended Actions:                                                  ║  │
│  ║  1. Begin local data center feasibility study                         ║  │
│  ║  2. Engage with RBI on transition timeline                            ║  │
│  ║  3. Notify affected member banks                                      ║  │
│  ╚═══════════════════════════════════════════════════════════════════════╝  │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  Type your compliance question...                              [Send] │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 8. TECH STACK

| Layer | Technology | Why |
|-------|------------|-----|
| **LLM** | Gemini Pro/Flash | Cost-effective, good structured output, Google ecosystem |
| **Database** | PostgreSQL + pgvector | Unified relational + vector store, ACID for compliance data |
| **Agent Framework** | PydanticAI + LangChain | Type-safe agents, RAG pipelines, tool integration |
| **Backend** | FastAPI (Python) | Async, fast, excellent LLM ecosystem |
| **Frontend** | Next.js + shadcn/ui | Modern, fast, great components |
| **Cache/Events** | Redis | Event bus, caching, real-time |
| **Task Queue** | Celery (optional) | Background agent tasks |

### Tech Stack Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND                                        │
│                            (Next.js)                                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │
│  │   Dashboard     │  │   GenUI Chat    │  │   Reports       │              │
│  │   (React)       │  │   (Streaming)   │  │   (PDF Gen)     │              │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘              │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │ HTTP/WebSocket
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              BACKEND                                         │
│                            (FastAPI)                                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │
│  │   REST API      │  │   WebSocket     │  │   Background    │              │
│  │   Endpoints     │  │   (Real-time)   │  │   Workers       │              │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘              │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                         AGENT LAYER                                    │  │
│  │                        (PydanticAI)                                    │  │
│  │  Agent 1  │  Agent 2  │  Agent 3  │  Agent 4  │  Agent 5             │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATA LAYER                                      │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌──────────────────────┐ │
│  │    PostgreSQL       │  │       Redis          │  │    Gemini API       │ │
│  │    + pgvector       │  │   (Cache + Events)   │  │    (LLM)            │ │
│  └─────────────────────┘  └─────────────────────┘  └──────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 9. MVP SCOPE (24-Hour Hackathon)

### Must Have (P0)

| Feature | Description | Demo Value |
|---------|-------------|------------|
| **Agent 3: Transaction Monitor** | Detect PAN patterns in sample data | Core detection capability |
| **Dashboard** | Compliance score, alerts, agent status | Visual proof |
| **GenUI Chat** | 3-4 sample queries working | Wow factor |
| **Mock Data** | Realistic transactions, violations | Believable demo |

### Should Have (P1)

| Feature | Description |
|---------|-------------|
| **Agent 1: Reg Monitor** | Parse one sample regulation |
| **Agent 2: Compliance Tracker** | Show member bank status |
| **Risk Heatmap** | Visual regulation risk |

### Nice to Have (P2)

| Feature | Description |
|---------|-------------|
| **Agent 4: Cross-Jurisdiction** | One multi-region example |
| **Agent 5: Report Generation** | Generate sample PDF |
| **Feedback Loop** | Basic approve/reject |

---

## 10. ALIGNMENT WITH VISA REQUIREMENTS

| Visa Requirement | AEGIS Feature | Status |
|------------------|---------------|--------|
| "Autonomous agents" | 5 specialized agents operating independently | ✅ |
| "Make decisions without supervision" | Agents detect, score, alert automatically | ✅ |
| "Break down complex objectives" | Multi-agent coordination | ✅ |
| "Access multiple data sources" | External regs + internal ecosystem data | ✅ |
| "Adapt based on feedback" | Feedback loop with pattern learning | ✅ |
| "Regulatory interpretation" | Agent 1 + LLM parsing | ✅ |
| "Policy mapping & gap detection" | Agent 2 obligations mapping | ✅ |
| "Real-time monitoring" | Agent 3 streaming analysis | ✅ |
| "Cross-regulatory analysis" | Agent 4 jurisdiction mapping | ✅ |
| "Natural language interaction" | GenUI chat interface | ✅ |
| "Dynamic dashboards" | AI-generated visualizations | ✅ |
| "Audit-ready evidence" | Agent 5 report generation | ✅ |
| "Minimal human intervention" | Autonomous detection + remediation | ✅ |

## 11. CRITICALITY SCORING MODEL

### Scoring Formula

```
CRITICALITY = f(URGENCY, IMPACT, EFFORT)

Where:
  URGENCY   = Time pressure based on due dates
  IMPACT    = Consequence severity if non-compliant
  EFFORT    = Difficulty of remediation

FORMULA:
  CRITICALITY = (URGENCY × 0.4) + (IMPACT × 0.4) + (10 - EFFORT) × 0.2

RESULT: Score 0-10, where 10 = Most Critical
```

### Urgency Calculation

```python
def calculate_urgency(due_date: date, is_hard_deadline: bool) -> float:
    """
    Calculate urgency score (0-10) based on time remaining
    
    Scenarios:
    1. External audit/regulatory deadline (hard)
    2. Internal policy deadline (soft)
    """
    days_remaining = (due_date - date.today()).days
    
    if days_remaining <= 0:
        return 10.0  # Already overdue
    elif days_remaining <= 7:
        return 9.0 if is_hard_deadline else 7.0
    elif days_remaining <= 14:
        return 8.0 if is_hard_deadline else 6.0
    elif days_remaining <= 30:
        return 6.0 if is_hard_deadline else 4.0
    elif days_remaining <= 90:
        return 4.0 if is_hard_deadline else 2.0
    else:
        return 2.0 if is_hard_deadline else 1.0
```

### Impact Scoring Matrix

| Factor | Low (1-3) | Medium (4-6) | High (7-10) |
|--------|-----------|--------------|-------------|
| **Financial Penalty** | <$100K | $100K-$1M | >$1M |
| **Reputational** | Internal only | Industry press | National news |
| **Scope (Entities)** | <10 affected | 10-100 affected | >100 affected |
| **Data Sensitivity** | Public data | Internal data | PII/PCI data |
| **Regulatory Response** | Warning | Investigation | Enforcement action |

### Two-Dimensional Risk Heatmap

```
TWO-DIMENSIONAL HEATMAP: CRITICALITY × DUE DATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                          DUE DATE (Days Remaining)
                    ┌──────────┬──────────┬──────────┬──────────┐
                    │   <7d    │  7-30d   │  30-90d  │   >90d   │
              ┌─────┼──────────┼──────────┼──────────┼──────────┤
              │ 9-10│    🔴    │    🔴    │    🟡    │    🟡    │
              │     │ CRITICAL │ CRITICAL │   HIGH   │ MODERATE │
              ├─────┼──────────┼──────────┼──────────┼──────────┤
  CRITICALITY │ 7-8 │    🔴    │    🟡    │    🟡    │    🟢    │
    SCORE     │     │ CRITICAL │   HIGH   │ MODERATE │   LOW    │
              ├─────┼──────────┼──────────┼──────────┼──────────┤
              │ 4-6 │    🟡    │    🟡    │    🟢    │    🟢    │
              │     │   HIGH   │ MODERATE │   LOW    │   LOW    │
              ├─────┼──────────┼──────────┼──────────┼──────────┤
              │ 1-3 │    🟡    │    🟢    │    🟢    │    🟢    │
              │     │ MODERATE │   LOW    │   LOW    │  MINIMAL │
              └─────┴──────────┴──────────┴──────────┴──────────┘

LEGEND:
  🔴 CRITICAL  = Immediate action required
  🟡 MODERATE  = Planned remediation, tracked
  🟢 LOW       = Monitor, schedule when convenient
```

---

## 12. CHAT ORCHESTRATOR PATTERN

### Architecture

The AI chatbot acts as an **orchestrator** that:
1. Understands user query
2. Calls appropriate function(s)
3. Aggregates results
4. Generates structured response

```
USER QUERY
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        LLM 1: QUERY UNDERSTANDING                            │
│                                                                              │
│  Input: "Which banks have expiring certifications and what's our PCI risk?" │
│                                                                              │
│  Output:                                                                     │
│  {                                                                           │
│    "intent": "multi_query",                                                  │
│    "sub_queries": [                                                          │
│      {"type": "entity_search", "params": {"cert_status": "expiring"}},       │
│      {"type": "risk_analysis", "params": {"regulation": "PCI-DSS"}}          │
│    ]                                                                         │
│  }                                                                           │
└────────────────────────────────────┬────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        FUNCTION ROUTER                                       │
│                                                                              │
│  Routes to appropriate tools based on intent:                                │
│                                                                              │
│  ┌───────────────────┐   ┌───────────────────┐   ┌───────────────────┐      │
│  │ search_entities() │   │ get_risk_score()  │   │ generate_report() │      │
│  └─────────┬─────────┘   └─────────┬─────────┘   └─────────┬─────────┘      │
│            │                       │                       │                 │
│            ▼                       ▼                       ▼                 │
│       entities[]              risk_data              report_content          │
│                                                                              │
└────────────────────────────────────┬────────────────────────────────────────┘
                                     │ Aggregate Results
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        LLM 2: RESPONSE GENERATION                            │
│                                                                              │
│  Input: {raw_results, original_query, user_context}                          │
│                                                                              │
│  Output: Structured JSON response                                            │
│  {                                                                           │
│    "text": "3 banks have expiring certifications...",                        │
│    "data": {                                                                 │
│      "expiring_banks": [...],                                                │
│      "pci_risk_score": 7.2,                                                  │
│      "risk_factors": [...]                                                   │
│    },                                                                        │
│    "suggested_actions": ["send_reminders", "view_details"],                  │
│    "visualizations": ["table", "risk_gauge"]                                 │
│  }                                                                           │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Available Functions

```python
ORCHESTRATOR_FUNCTIONS = {
    # Entity Operations
    "search_entities": "Filter member banks/merchants by criteria",
    "get_entity_details": "Get full compliance record for entity",
    "update_entity_status": "Mark status change (requires approval)",
    
    # Violation Operations
    "list_violations": "Get violations with filters",
    "get_violation_details": "Full violation record with evidence",
    "acknowledge_violation": "Mark as reviewed",
    
    # Risk Operations
    "get_risk_score": "Overall or per-regulation risk score",
    "get_risk_heatmap": "2D heatmap data",
    "explain_risk": "LLM explanation of risk factors",
    
    # Regulation Operations
    "search_regulations": "Semantic search across regulations",
    "get_regulation_impact": "Entities affected by regulation",
    "check_compliance": "Compare entity vs regulation requirements",
    
    # Reporting
    "generate_report": "Create compliance report",
    "generate_evidence_package": "Audit-ready evidence",
    "get_remediation_tasks": "Task list for violation",
    
    # Rule Management (via chat)
    "list_active_rules": "Show rules currently monitored",
    "disable_rule": "Temporarily disable a detection rule",
    "explain_rule": "Why this rule exists, what it detects",
}
```

### Response Format

```python
class ChatResponse(BaseModel):
    text: str                           # Human-readable response
    data: Optional[dict]                # Structured data for UI
    suggested_actions: List[str]        # Action buttons to show
    visualizations: List[str]           # UI components to render
    confidence: float                   # 0-1 confidence in response
    sources: List[str]                  # Citations (regulation IDs)
```

---

## 13. REMEDIATION TASK LISTS

### Output Format

When a violation is detected, Agent 5 generates structured task lists:

```json
{
  "violation_id": "VIO-2026-001",
  "violation_type": "PCI-DSS 3.4 - PAN in logs",
  "criticality_score": 9,
  "due_date": "2026-01-12",
  
  "short_term_fixes": [
    {
      "task_id": "ST-001",
      "title": "Sanitize existing logs containing PANs",
      "owner_role": "Security Team",
      "estimated_hours": 4,
      "deadline": "2026-01-06",
      "priority": "P0",
      "steps": [
        {
          "step": 1,
          "action": "Identify all log files from last 30 days",
          "command": "find /var/log -name '*.log' -mtime -30",
          "expected_output": "List of log files"
        },
        {
          "step": 2,
          "action": "Run regex pattern to find PANs",
          "pattern": "\\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14})\\b",
          "tool": "grep -r -E '{pattern}' /var/log"
        },
        {
          "step": 3,
          "action": "Replace with masked format",
          "format": "****-****-****-XXXX (last 4 only)",
          "verification": "Re-run grep, expect 0 matches"
        },
        {
          "step": 4,
          "action": "Document sanitization in audit log",
          "template": "SANITIZATION_RECORD"
        }
      ],
      "verification": {
        "method": "Re-scan with same pattern",
        "expected": "0 matches",
        "auditor_signoff_required": true
      }
    },
    {
      "task_id": "ST-002",
      "title": "Notify affected merchant",
      "owner_role": "Relationship Manager",
      "estimated_hours": 1,
      "deadline": "2026-01-05",
      "priority": "P0",
      "template": "MERCHANT_VIOLATION_NOTIFICATION"
    }
  ],
  
  "long_term_solutions": [
    {
      "task_id": "LT-001",
      "title": "Implement automated log sanitization pipeline",
      "owner_role": "Engineering",
      "estimated_weeks": 2,
      "priority": "P1",
      "phases": [
        {
          "phase": 1,
          "title": "Design",
          "duration": "2 days",
          "deliverable": "Architecture design document"
        },
        {
          "phase": 2,
          "title": "Development",
          "duration": "5 days",
          "deliverable": "Sanitization service code"
        },
        {
          "phase": 3,
          "title": "Testing",
          "duration": "2 days",
          "deliverable": "Test report with edge cases"
        },
        {
          "phase": 4,
          "title": "Deployment",
          "duration": "1 day",
          "deliverable": "Production deployment"
        }
      ],
      "success_criteria": [
        "All PANs masked within 100ms of log ingestion",
        "Zero false negatives in test suite",
        "Audit log of all sanitizations"
      ]
    },
    {
      "task_id": "LT-002",
      "title": "Update logging policy and train developers",
      "owner_role": "Compliance + Engineering",
      "estimated_weeks": 1,
      "deliverables": [
        "Updated logging policy document",
        "Developer training session (recorded)",
        "Pre-commit hook to block PAN logging"
      ]
    }
  ],
  
  "evidence_required": [
    "Screenshot of sanitized logs",
    "Scan report showing 0 violations",
    "Audit trail of remediation actions",
    "Sign-off from compliance officer"
  ]
}
```

### Task List Data Structure

```python
class RemediationStep(BaseModel):
    step: int
    action: str
    command: Optional[str]
    tool: Optional[str]
    expected_output: Optional[str]
    verification: Optional[str]

class RemediationTask(BaseModel):
    task_id: str
    title: str
    owner_role: str
    estimated_hours: Optional[int]
    estimated_weeks: Optional[int]
    deadline: Optional[date]
    priority: str  # "P0", "P1", "P2"
    steps: Optional[List[RemediationStep]]
    phases: Optional[List[dict]]
    deliverables: Optional[List[str]]
    success_criteria: Optional[List[str]]
    verification: Optional[dict]

class RemediationPlan(BaseModel):
    violation_id: str
    violation_type: str
    criticality_score: float
    due_date: date
    short_term_fixes: List[RemediationTask]
    long_term_solutions: List[RemediationTask]
    evidence_required: List[str]
```

---

## 14. VECTORIZED RULES ENGINE

### Why Vectorization for Rules?

```
TRADITIONAL APPROACH:
───────────────────────────────────────────
for each transaction:
    for each rule in rules:  # 500+ rules
        if rule.matches(transaction):
            violations.append(...)

PROBLEM: O(n × m) where n=transactions, m=rules
         With 1M transactions × 500 rules = 500M checks
```

```
VECTORIZED APPROACH:
───────────────────────────────────────────
1. Pre-compute rule embeddings (once)
2. Batch embed transactions
3. Vector similarity to find relevant rules
4. Only run matching rules

BENEFIT: O(n × log(m)) with vector index
         Much faster for large rule sets
```

### Rules Table Schema

```sql
CREATE TABLE detection_rules (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            VARCHAR(255) NOT NULL,
    description     TEXT NOT NULL,
    regulation_id   UUID REFERENCES regulations(id),
    category        VARCHAR(50) NOT NULL,  -- 'PAN_DETECTION', 'ACCESS_ANOMALY', etc.
    
    -- Rule Definition
    rule_type       VARCHAR(50) NOT NULL,  -- 'REGEX', 'SEMANTIC', 'ML', 'COMPOSITE'
    pattern         TEXT,                   -- Regex pattern if applicable
    threshold       FLOAT,                  -- For anomaly detection
    
    -- Vectorized Matching
    embedding       vector(768),            -- Rule description embedding
    
    -- Applicability
    applies_to      TEXT[],                 -- ['transaction_logs', 'settlements', etc.]
    jurisdictions   TEXT[],                 -- ['US', 'EU', 'GLOBAL']
    entity_types    TEXT[],                 -- ['bank', 'merchant', 'processor']
    
    -- Control
    is_active       BOOLEAN DEFAULT true,
    disabled_until  TIMESTAMP,              -- Temporary disable
    disabled_by     VARCHAR(100),
    disabled_reason TEXT,
    
    -- Metadata
    severity        VARCHAR(20) NOT NULL,   -- 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP,
    version         INT DEFAULT 1
);

-- Index for vector search
CREATE INDEX idx_rules_embedding ON detection_rules 
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);
```

### Rule Matching Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ FLOW: PARALLEL RULE MATCHING                                                 │
│ Trigger: New data batch received                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. Data batch arrives (e.g., 1000 transactions)                             │
│     │                                                                        │
│     ▼                                                                        │
│  2. Classify data type                                                       │
│     │   └── "transaction_logs" → filter rules by applies_to                  │
│     │                                                                        │
│  3. Get applicable rules                                                     │
│     │   └── SELECT * FROM detection_rules                                    │
│     │       WHERE 'transaction_logs' = ANY(applies_to)                       │
│     │       AND is_active = true                                             │
│     │       AND (disabled_until IS NULL OR disabled_until < NOW())           │
│     │                                                                        │
│  4. PARALLEL EXECUTION (batch processing)                                    │
│     │                                                                        │
│     ├── REGEX RULES (Layer 1)                                                │
│     │   └── Run all regex patterns in parallel                               │
│     │   └── Vectorized string matching (numpy/pandas)                        │
│     │   └── Returns: immediate_violations[]                                  │
│     │                                                                        │
│     ├── SEMANTIC RULES (Layer 2)                                             │
│     │   └── Embed data samples that passed Layer 1                           │
│     │   └── Vector similarity against rule embeddings                        │
│     │   └── Returns: potential_violations[]                                  │
│     │                                                                        │
│     └── LLM RULES (Layer 3) - only for flagged items                         │
│         └── Send to Gemini for complex analysis                              │
│         └── Returns: confirmed_violations[] + explanations                   │
│                                                                              │
│  5. Aggregate results, calculate criticality scores                          │
│                                                                              │
│  6. Store violations, emit events                                            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Rule Disable via Chat

```
USER: "Disable the PAN detection rule for BNK-123 for 24 hours, 
       they're doing a planned data migration"

ORCHESTRATOR:
1. Parse: {action: "disable_rule", rule: "PAN_DETECTION", 
           entity: "BNK-123", duration: "24h", reason: "planned migration"}

2. Validate: User has permission? Entity exists? Duration reasonable?

3. Execute:
   UPDATE detection_rules 
   SET disabled_until = NOW() + INTERVAL '24 hours',
       disabled_by = 'user@visa.com',
       disabled_reason = 'Planned data migration for BNK-123'
   WHERE name = 'PAN_DETECTION';
   
   -- Also log to audit
   INSERT INTO rule_audit_log (...) VALUES (...);

4. Response: "PAN detection rule disabled for BNK-123 until 
              2026-01-06 03:30 UTC. Audit logged."
```

---

## 15. DATABASE SCHEMA (Complete)

### Core Tables

```sql
-- Regulatory Sources (Admin-managed)
CREATE TABLE regulatory_sources (...);  -- Defined in Agent 1 section

-- Regulations
CREATE TABLE regulations (
    id              UUID PRIMARY KEY,
    source_id       UUID REFERENCES regulatory_sources(id),
    title           VARCHAR(500) NOT NULL,
    summary         TEXT,
    full_text       TEXT,
    region          VARCHAR(50),
    sector          VARCHAR(50),
    effective_date  DATE,
    compliance_deadline DATE,
    version         VARCHAR(50),
    content_hash    TEXT,
    embedding       vector(768),
    fetched_at      TIMESTAMP,
    created_at      TIMESTAMP DEFAULT NOW()
);

-- Obligations (extracted from regulations)
CREATE TABLE obligations (
    id              UUID PRIMARY KEY,
    regulation_id   UUID REFERENCES regulations(id),
    text            TEXT NOT NULL,
    category        VARCHAR(100),
    applies_to      TEXT[],
    effective_date  DATE,
    embedding       vector(768)
);

-- Detection Rules
CREATE TABLE detection_rules (...);  -- Defined in Section 14

-- Entities (Member Banks, Merchants, Vendors)
CREATE TABLE entities (
    id              UUID PRIMARY KEY,
    external_id     VARCHAR(100) UNIQUE,  -- BNK-1234, MID-5678
    name            VARCHAR(255) NOT NULL,
    type            VARCHAR(50) NOT NULL,  -- 'bank', 'merchant', 'vendor'
    region          VARCHAR(50),
    
    -- Compliance Status
    pci_status      VARCHAR(50),  -- 'valid', 'expiring', 'expired'
    pci_expiry_date DATE,
    last_audit_date DATE,
    risk_score      FLOAT,
    
    -- Relationship
    relationship_manager UUID,
    
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP
);

-- Violations/Findings
CREATE TABLE violations (
    id              UUID PRIMARY KEY,
    entity_id       UUID REFERENCES entities(id),
    rule_id         UUID REFERENCES detection_rules(id),
    regulation_id   UUID REFERENCES regulations(id),
    
    -- Details
    severity        VARCHAR(20) NOT NULL,
    title           VARCHAR(255) NOT NULL,
    description     TEXT,
    evidence        JSONB,  -- {log_snippet, screenshot_path, etc.}
    
    -- Criticality
    criticality_score FLOAT,
    urgency_score   FLOAT,
    impact_score    FLOAT,
    due_date        DATE,
    is_hard_deadline BOOLEAN DEFAULT false,
    
    -- Status
    status          VARCHAR(50) DEFAULT 'open',  -- 'open', 'investigating', 'remediated', 'false_positive'
    acknowledged_by VARCHAR(100),
    acknowledged_at TIMESTAMP,
    resolved_at     TIMESTAMP,
    
    -- Timestamps
    detected_at     TIMESTAMP DEFAULT NOW(),
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP
);

-- Remediation Tasks
CREATE TABLE remediation_tasks (
    id              UUID PRIMARY KEY,
    violation_id    UUID REFERENCES violations(id),
    
    task_type       VARCHAR(50),  -- 'short_term', 'long_term'
    title           VARCHAR(255) NOT NULL,
    owner_role      VARCHAR(100),
    assigned_to     VARCHAR(100),
    
    estimated_hours INT,
    deadline        DATE,
    priority        VARCHAR(10),  -- 'P0', 'P1', 'P2'
    
    steps           JSONB,  -- Array of step objects
    
    status          VARCHAR(50) DEFAULT 'pending',
    completed_at    TIMESTAMP,
    
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP
);

-- Alerts
CREATE TABLE alerts (
    id              UUID PRIMARY KEY,
    type            VARCHAR(100) NOT NULL,
    severity        VARCHAR(20) NOT NULL,
    title           VARCHAR(255) NOT NULL,
    description     TEXT,
    
    related_entity  UUID REFERENCES entities(id),
    related_violation UUID REFERENCES violations(id),
    related_regulation UUID REFERENCES regulations(id),
    
    is_read         BOOLEAN DEFAULT false,
    is_dismissed    BOOLEAN DEFAULT false,
    
    created_at      TIMESTAMP DEFAULT NOW()
);

-- Audit Log (Immutable)
CREATE TABLE audit_log (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp       TIMESTAMP DEFAULT NOW(),
    actor           VARCHAR(100) NOT NULL,  -- User or 'AGENT_1', 'AGENT_3', etc.
    action          VARCHAR(100) NOT NULL,
    resource_type   VARCHAR(100),
    resource_id     UUID,
    details         JSONB,
    ip_address      INET
);

-- Chat History
CREATE TABLE chat_history (
    id              UUID PRIMARY KEY,
    session_id      UUID NOT NULL,
    user_id         VARCHAR(100),
    
    query           TEXT NOT NULL,
    response        JSONB NOT NULL,  -- Full ChatResponse object
    
    functions_called TEXT[],
    latency_ms      INT,
    
    created_at      TIMESTAMP DEFAULT NOW()
);
```

### Indexes for Performance

```sql
-- Vector indexes
CREATE INDEX idx_regulations_embedding ON regulations USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_obligations_embedding ON obligations USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_rules_embedding ON detection_rules USING ivfflat (embedding vector_cosine_ops);

-- Query indexes
CREATE INDEX idx_violations_status ON violations(status);
CREATE INDEX idx_violations_severity ON violations(severity);
CREATE INDEX idx_violations_due_date ON violations(due_date);
CREATE INDEX idx_entities_type ON entities(type);
CREATE INDEX idx_entities_pci_status ON entities(pci_status);
CREATE INDEX idx_alerts_created ON alerts(created_at DESC);
```

---

## 16. SECURITY CONSIDERATIONS

### TODO: Security Assessment Required

> 🔒 These items require detailed security analysis before production:

| Area | Risk | Mitigation (TODO) |
|------|------|-------------------|
| **URL Scraping** | Prompt injection via malicious regulatory content | Sandbox scraping, content sanitization |
| **LLM Outputs** | Hallucination in compliance advice | Human review for critical actions |
| **Rule Disable via Chat** | Unauthorized disabling of detection | Role-based permissions, audit logging |
| **Evidence Tampering** | Modification of violation evidence | Append-only storage, hash verification |
| **Cross-tenant Data** | Bank A seeing Bank B's violations | Row-level security, strict isolation |
| **API Access** | Unauthorized data access | OAuth2, rate limiting, audit logs |
| **Agent Autonomy** | Agent takes harmful action | Approval workflows for Level 3+ actions |

### Autonomy Levels with Security

```
LEVEL 1: DETECT & ALERT (MVP)
├── Agent can: Detect, score, alert
├── Agent cannot: Take any action
└── Security: Low risk

LEVEL 2: RECOMMEND (Target)
├── Agent can: Suggest remediation, draft tasks
├── Agent cannot: Execute changes
└── Security: Medium risk (review LLM outputs)

LEVEL 3: ACT WITH APPROVAL
├── Agent can: Prepare action, request approval
├── Human must: Click approve
└── Security: Gated by human

LEVEL 4+: FUTURE (Not for hackathon)
├── Requires: Full security audit
└── Risk: High
```

---

## 17. NEXT STEPS

### Immediate (Hackathon)

1. [ ] Set up project structure (monorepo: `backend/`, `frontend/`)
2. [ ] Create database schema (PostgreSQL + pgvector)
3. [ ] Implement Agent 3 (Transaction Monitor) - core demo
4. [ ] Build basic dashboard (4 screens)
5. [ ] Create mock data (entities, violations, alerts)
6. [ ] Implement chat orchestrator (basic functions)
7. [ ] Add criticality scoring + 2D heatmap

### Before Demo

1. [ ] Implement Agent 1 (scheduled fetch from 2-3 sources)
2. [ ] Implement Agent 2 (entity compliance tracking)
3. [ ] Add remediation task list generation
4. [ ] Polish UI
5. [ ] Create demo script
6. [ ] Record backup demo video

### Production (Post-Hackathon)

1. [ ] Security assessment (all TODO items)
2. [ ] Real regulatory source integrations
3. [ ] Agent 4 (Cross-Jurisdiction)
4. [ ] Agent 5 (Evidence Generation)
5. [ ] Multi-tenant architecture
6. [ ] Authentication + RBAC
7. [ ] Performance optimization

---

*Document Version: 3.0 | January 5, 2026*
*Author: Mudassir | AEGIS Team*
*Visa Hackathon - Problem Statement 4*
