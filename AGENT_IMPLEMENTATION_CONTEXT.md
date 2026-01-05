# Agent Implementation Context
## For Parallel Implementation by Multiple Agents

> **CRITICAL:** Each agent has SEPARATE files. Do NOT modify files owned by other agents.
> **Reference:** Use Agent 3 (`agents/transaction_monitor.py`) as the pattern.

---

## ⚠️ TESTING PROTOCOL (READ FIRST!)

### DO NOT restart the running servers!
```
Frontend: http://localhost:3000 (ALREADY RUNNING - don't touch)
Backend:  http://localhost:8000 (ALREADY RUNNING - don't restart)
```

### How Testing Works
1. **Servers have `--reload` flag** - they auto-detect file changes
2. When you add/modify files, uvicorn reloads automatically
3. **NO NEED to run** `python -m uvicorn` yourself

### For Your Testing
```bash
# ✅ DO: Use curl to test your endpoints
curl http://localhost:8000/api/your-endpoint

# ✅ DO: Check Swagger UI
# Open http://localhost:8000/docs in browser

# ❌ DON'T: Start new server instances
# ❌ DON'T: Run `npm run dev` or `uvicorn` commands
```

### If Server Is Down
Ask the **Coordinator Agent** to restart servers.
Only ONE agent should manage server lifecycle.

### Browser Testing
- Use existing browser tabs at localhost:3000
- Navigate to pages as needed
- Don't start new dev servers

---

## 🔒 RESOURCE LOCKS (CHECK FIRST!)

**Before using shared resources, check:** `RESOURCE_LOCKS.md`

### Self-Check Protocol:
1. **Read** `RESOURCE_LOCKS.md`
2. **Check** if resource is 🟢 FREE or 🔴 LOCKED
3. **Update** status to LOCKED with your agent name when using
4. **Update** back to FREE when done

### Shared Resources That Need Locking:
- `routes/__init__.py` (multiple agents may need to add imports)
- `agents/__init__.py` (multiple agents may need to add imports)  
- `main.py` (if adding routers)
- Browser sessions (for visual testing)

---

## FILE OWNERSHIP (NO CONFLICTS)

| Agent Thread | Files to CREATE | Files to MODIFY |
|--------------|-----------------|-----------------|
| **Agent 1** | `agents/regulatory_monitor.py` | `routes/__init__.py` (add import) |
| **Agent 2** | `agents/ecosystem_tracker.py` | `routes/__init__.py` (add import) |
| **Agent 4** | `agents/cross_jurisdiction.py` | `routes/__init__.py` (add import) |
| **Agent 5** | `agents/evidence_engine.py` | `routes/__init__.py` (add import) |

---

## AGENT 1: REGULATORY INTELLIGENCE MONITOR

### Purpose
Monitor regulatory sources for updates, parse changes, alert on new regulations.

### Implementation Requirements
```python
# File: backend/agents/regulatory_monitor.py

class RegulatoryMonitor:
    """Monitor regulatory sources and detect changes"""
    
    def __init__(self):
        # Store known regulation hashes for change detection
        self.regulation_hashes = {}
    
    def fetch_source(self, source_url: str, method: str = "mock") -> dict:
        """
        Fetch content from regulatory source
        For hackathon: Return mock data, don't actually scrape
        Returns: {content: str, hash: str, timestamp: str}
        """
        pass
    
    def detect_changes(self, source_id: str, new_hash: str) -> bool:
        """Compare hash with stored version"""
        pass
    
    def parse_regulation(self, content: str) -> dict:
        """
        Use LLM to extract structured obligations
        Returns: {title, summary, obligations[], effective_date}
        """
        pass
    
    def calculate_impact(self, regulation: dict) -> dict:
        """
        Determine affected entities
        Returns: {affected_count, entity_ids[], urgency}
        """
        pass
```

### Mock Data to Return
```python
MOCK_REGULATIONS = [
    {
        "id": "REG-2026-001",
        "title": "GDPR Amendment - AI Act Integration",
        "source": "europa.eu",
        "region": "EU",
        "summary": "New requirements for AI systems processing personal data",
        "effective_date": "2026-03-01",
        "status": "new",
        "impact": "high",
        "affected_entities": 234
    },
    {
        "id": "REG-2026-002", 
        "title": "RBI Data Localization Update",
        "source": "rbi.org.in",
        "region": "IN",
        "summary": "Extended compliance deadline for payment data storage",
        "effective_date": "2026-06-30",
        "status": "updated",
        "impact": "medium",
        "affected_entities": 12
    }
]
```

### API Route to Add
```python
# Add to routes/regulations.py (NEW FILE)
from fastapi import APIRouter
router = APIRouter(prefix="/api/regulations", tags=["regulations"])

@router.get("/")
def list_regulations(region: str = None, status: str = None):
    """List all tracked regulations with filters"""
    
@router.get("/{regulation_id}")
def get_regulation(regulation_id: str):
    """Get full regulation details"""
    
@router.get("/{regulation_id}/impact")
def get_regulation_impact(regulation_id: str):
    """Get entities affected by this regulation"""

@router.post("/check-updates")
def check_for_updates():
    """Trigger a check for regulatory updates (demo)"""
```

---

## AGENT 2: ECOSYSTEM COMPLIANCE TRACKER

### Purpose
Track compliance status of member banks, merchants, vendors. Alert on expiring certifications.

### Implementation Requirements
```python
# File: backend/agents/ecosystem_tracker.py

class EcosystemTracker:
    """Track compliance status of ecosystem entities"""
    
    def get_entity_compliance(self, entity_id: str) -> dict:
        """
        Get full compliance record for entity
        Returns: {entity, certifications[], violations[], risk_score}
        """
        pass
    
    def check_expiring_certifications(self, days: int = 30) -> list:
        """
        Find entities with certs expiring within N days
        Returns: [{entity_id, cert_type, expiry_date, days_remaining}]
        """
        pass
    
    def calculate_entity_risk(self, entity_id: str) -> float:
        """
        Calculate risk score based on:
        - Certification status
        - Violation history
        - Transaction volume
        Returns: 0.0 - 10.0 score
        """
        pass
    
    def generate_reminder(self, entity_id: str, reminder_type: str) -> dict:
        """
        Generate compliance reminder notification
        Returns: {recipient, subject, body, urgency}
        """
        pass
```

### Mock Data (extends existing mock_data.py)
```python
ENTITY_CERTIFICATIONS = {
    "BNK-1234": [
        {"type": "PCI-DSS", "level": "Level 1", "expiry": "2026-01-15", "status": "expiring"},
        {"type": "SOC2", "expiry": "2026-08-01", "status": "valid"}
    ],
    "MID-4521": [
        {"type": "PCI-DSS", "level": "SAQ-A", "expiry": "2026-03-15", "status": "valid"}
    ]
}
```

### API Endpoints (extend routes/entities.py)
```python
@router.get("/{entity_id}/certifications")
def get_entity_certifications(entity_id: str):
    """Get all certifications for an entity"""

@router.get("/expiring")
def get_expiring_certifications(days: int = 30):
    """Get all entities with expiring certs"""

@router.post("/{entity_id}/send-reminder")
def send_reminder(entity_id: str, reminder_type: str):
    """Send compliance reminder (demo - just returns what would be sent)"""
```

---

## AGENT 4: CROSS-JURISDICTION ANALYZER

### Purpose
Analyze transactions crossing multiple regulatory jurisdictions. Identify conflicts.

### Implementation Requirements
```python
# File: backend/agents/cross_jurisdiction.py

class CrossJurisdictionAnalyzer:
    """Analyze cross-border compliance requirements"""
    
    # Jurisdiction → Applicable Regulations mapping
    JURISDICTION_REGS = {
        "EU": ["GDPR", "PSD2", "DORA"],
        "US": ["CCPA", "GLBA", "SOX"],
        "IN": ["RBI-DL", "PDPB", "IT-ACT"],
        "SG": ["PDPA", "MAS-TRM"],
        "GLOBAL": ["PCI-DSS", "ISO-27001"]
    }
    
    def analyze_transaction(self, transaction: dict) -> dict:
        """
        Analyze a transaction's cross-jurisdiction compliance
        Input: {origin_country, processor_country, settlement_country, data_types}
        Output: {jurisdictions[], applicable_regs[], conflicts[], guidance}
        """
        pass
    
    def check_data_flow_compliance(self, origin: str, destination: str) -> dict:
        """
        Check if data can legally flow between jurisdictions
        Returns: {allowed: bool, requirements[], warnings[]}
        """
        pass
    
    def get_jurisdiction_conflicts(self, jurisdictions: list) -> list:
        """
        Find conflicting requirements between jurisdictions
        Returns: [{reg_a, reg_b, conflict_type, resolution}]
        """
        pass
```

### Mock Analysis Output
```python
SAMPLE_ANALYSIS = {
    "transaction_id": "TXN-2026-001",
    "jurisdictions": ["EU-GDPR", "SG-PDPA", "US-CCPA"],
    "applicable_rules": [
        "GDPR Art 44-49: Cross-border transfer requirements",
        "PDPA: Data processing obligations", 
        "CCPA: Consumer rights notification"
    ],
    "compliance_status": "COMPLIANT",
    "conditions": [
        "Standard Contractual Clauses must be in place",
        "Data Processing Agreement required"
    ],
    "risks": [
        "GDPR adequacy decision may change",
        "Singapore regulations under review"
    ]
}
```

### API Route (NEW FILE)
```python
# routes/jurisdiction.py
@router.post("/analyze")
def analyze_transaction(transaction: TransactionAnalysisRequest):
    """Analyze cross-jurisdiction compliance for a transaction"""

@router.get("/check-data-flow")
def check_data_flow(origin: str, destination: str):
    """Check if data can flow between two jurisdictions"""

@router.get("/conflicts")
def get_known_conflicts():
    """List known regulatory conflicts"""
```

---

## AGENT 5: EVIDENCE & REPORTING ENGINE

### Purpose
Generate audit-ready evidence packages. Create remediation task lists.

### Implementation Requirements
```python
# File: backend/agents/evidence_engine.py

class EvidenceEngine:
    """Generate audit evidence and remediation plans"""
    
    def compile_evidence_package(self, violation_id: str) -> dict:
        """
        Create audit-ready evidence package for a violation
        Returns: {
            violation_summary,
            timeline,
            evidence_items[],
            remediation_status,
            sign_offs[]
        }
        """
        pass
    
    def generate_remediation_plan(self, violation_id: str) -> dict:
        """
        Generate step-by-step remediation tasks
        Returns: {
            short_term_fixes[],
            long_term_solutions[],
            estimated_effort,
            deadlines
        }
        """
        pass
    
    def generate_report(self, report_type: str, scope: dict) -> dict:
        """
        Generate compliance report
        report_type: 'executive_summary', 'full_audit', 'regulation_specific'
        Returns: {title, sections[], generated_at}
        """
        pass
```

### Task List Output Format
```python
SAMPLE_REMEDIATION_PLAN = {
    "violation_id": "VIO-2026-001",
    "criticality": 9,
    "short_term_fixes": [
        {
            "task_id": "ST-001",
            "title": "Sanitize logs containing PANs",
            "owner": "Security Team",
            "estimated_hours": 4,
            "deadline": "2026-01-06",
            "steps": [
                "Identify affected log files",
                "Run regex scan for PANs",
                "Apply masking script",
                "Verify no PANs remain"
            ]
        }
    ],
    "long_term_solutions": [
        {
            "task_id": "LT-001", 
            "title": "Implement log sanitization pipeline",
            "owner": "Engineering",
            "estimated_weeks": 2,
            "phases": ["Design", "Development", "Testing", "Deploy"]
        }
    ]
}
```

### API Route (NEW FILE)
```python
# routes/evidence.py
@router.get("/violations/{violation_id}/evidence")
def get_evidence_package(violation_id: str):
    """Get audit evidence for a violation"""

@router.get("/violations/{violation_id}/remediation")
def get_remediation_plan(violation_id: str):
    """Get remediation task list"""

@router.post("/reports/generate")
def generate_report(report_type: str, scope: ReportScope):
    """Generate a compliance report"""
```

---

## SHARED UTILITIES (agents/__init__.py)

Add these shared imports for all agents:
```python
# agents/__init__.py
from .transaction_monitor import TransactionMonitor
from .regulatory_monitor import RegulatoryMonitor  # Agent 1
from .ecosystem_tracker import EcosystemTracker    # Agent 2
from .cross_jurisdiction import CrossJurisdictionAnalyzer  # Agent 4
from .evidence_engine import EvidenceEngine        # Agent 5
```

---

## INTEGRATION WITH MAIN APP

After all agents are created, update `main.py`:
```python
# Add these imports
from routes import regulations, jurisdiction, evidence

# Add these routers
app.include_router(regulations.router)
app.include_router(jurisdiction.router)
app.include_router(evidence.router)
```

---

## TESTING CHECKLIST

Each agent should work standalone:
```bash
# Test Agent 1
curl http://localhost:8000/api/regulations/
curl http://localhost:8000/api/regulations/REG-2026-001

# Test Agent 2  
curl http://localhost:8000/api/entities/BNK-1234/certifications
curl http://localhost:8000/api/entities/expiring?days=30

# Test Agent 4
curl -X POST http://localhost:8000/api/jurisdiction/analyze -d '{"origin": "DE", "destination": "US"}'

# Test Agent 5
curl http://localhost:8000/api/violations/VIO-2026-001/evidence
curl http://localhost:8000/api/violations/VIO-2026-001/remediation
```

---

## SESSION LOGGING

After implementation, each agent thread should add to AGENT_COORDINATION.md:
```markdown
## Session Log
Date: YYYY-MM-DD HH:MM
Agent: [Agent 1/2/4/5]
Conversation ID: [id]

### Work Completed
- [x] Created agents/[name].py
- [x] Created routes/[name].py  
- [x] Updated agents/__init__.py
- [x] Tested endpoints

### Handoff Notes
- [notes]
```
