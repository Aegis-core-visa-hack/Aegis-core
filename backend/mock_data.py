"""Mock data for AEGIS backend - mirrors frontend mockData.ts"""
from datetime import datetime, timedelta


# Dashboard data
dashboard_summary = {
    "compliance_score": {"value": 78, "change": 3, "trend": "up"},
    "at_risk_entities": {"value": 12, "change": -2, "trend": "down"},
    "violations_24h": {"value": 47, "change": 8, "trend": "up"},
    "agents_online": 5,
    "agents_total": 5,
}

agents = [
    {
        "id": 1,
        "name": "agent_1_regulatory",
        "display_name": "Regulatory Intelligence",
        "status": "online",
        "last_run": "5 min ago",
        "description": "Monitors regulatory sources for new compliance requirements",
    },
    {
        "id": 2,
        "name": "agent_2_ecosystem",
        "display_name": "Ecosystem Tracker",
        "status": "online",
        "last_run": "10 min ago",
        "description": "Tracks member bank and merchant compliance status",
    },
    {
        "id": 3,
        "name": "agent_3_transaction",
        "display_name": "Transaction Monitor",
        "status": "running",
        "last_run": "now",
        "description": "Real-time monitoring for PCI/PII violations",
        "stats": "2.3M tx/hour",
    },
    {
        "id": 4,
        "name": "agent_4_jurisdiction",
        "display_name": "Cross-Jurisdiction",
        "status": "online",
        "last_run": "1 hour ago",
        "description": "Analyzes cross-border compliance requirements",
    },
    {
        "id": 5,
        "name": "agent_5_reporting",
        "display_name": "Evidence Engine",
        "status": "online",
        "last_run": "30 min ago",
        "description": "Generates audit-ready reports and evidence packages",
    },
]

risk_heatmap = [
    {"name": "PCI-DSS", "risk_level": "high", "score": 72, "open_violations": 12, "jurisdiction": "Global"},
    {"name": "GDPR", "risk_level": "medium", "score": 85, "open_violations": 8, "jurisdiction": "EU"},
    {"name": "RBI", "risk_level": "medium", "score": 81, "open_violations": 3, "jurisdiction": "IN"},
    {"name": "CCPA", "risk_level": "low", "score": 94, "open_violations": 1, "jurisdiction": "US-CA"},
    {"name": "LGPD", "risk_level": "low", "score": 91, "open_violations": 2, "jurisdiction": "BR"},
]

# Alerts data
alerts = [
    {
        "id": "ALT-001",
        "severity": "critical",
        "title": "Transaction anomaly detected",
        "description": "Unusual volume spike from Merchant MID-4521",
        "timestamp": "2026-01-05T09:14:00Z",
        "entity_id": "MID-4521",
        "regulation": "PCI-DSS",
        "status": "open",
    },
    {
        "id": "ALT-002",
        "severity": "critical",
        "title": "PAN detected in settlement log",
        "description": "Full card number found in plaintext",
        "timestamp": "2026-01-05T08:45:00Z",
        "entity_id": "MID-4521",
        "regulation": "PCI-DSS 3.4",
        "status": "open",
    },
    {
        "id": "ALT-003",
        "severity": "high",
        "title": "Bank certification expiring",
        "description": "BNK-123 PCI certification expires in 5 days",
        "timestamp": "2026-01-05T08:30:00Z",
        "entity_id": "BNK-123",
        "regulation": "PCI-DSS",
        "status": "open",
    },
    {
        "id": "ALT-004",
        "severity": "medium",
        "title": "GDPR amendment published",
        "description": "New data retention requirements - impact analysis pending",
        "timestamp": "2026-01-05T07:15:00Z",
        "entity_id": None,
        "regulation": "GDPR",
        "status": "investigating",
    },
    {
        "id": "ALT-005",
        "severity": "low",
        "title": "Vendor assessment due",
        "description": "Annual review for VND-456 due in 30 days",
        "timestamp": "2026-01-05T06:00:00Z",
        "entity_id": "VND-456",
        "regulation": "PCI-DSS",
        "status": "open",
    },
]

# Alert details (keyed by ID)
alert_details = {
    "ALT-001": {
        "id": "ALT-001",
        "severity": "critical",
        "title": "Transaction Anomaly Detected",
        "description": "Unusual volume spike from Merchant MID-4521",
        "timestamp": "2026-01-05T09:14:00Z",
        "entity_id": "MID-4521",
        "regulation": "PCI-DSS",
        "status": "open",
        "evidence": """Anomaly Detection Report:

Merchant: ElectroMart Inc (MID-4521)
Time Window: 2026-01-05 08:00 - 09:00

Baseline (30-day avg): 1,076 transactions/hour
Current Period: 4,521 transactions/hour
Deviation: 4.2x higher than normal

Geographic Distribution:
- 78% from new countries (RU, UA, BY)
- Previous: 95% US, 5% CA

Decline Rate:
- Current: 34% (normal: 6%)

VERDICT: Pattern consistent with card testing attack""",
        "recommendations": [
            "Immediately review transaction batch for fraudulent patterns",
            "Consider temporary suspension pending investigation",
            "Notify acquiring bank for coordinated response",
            "Preserve all transaction logs for forensic analysis",
        ],
        "context": {
            "similar_violations": 0,
            "entity_name": "ElectroMart Inc",
            "entity_volume": "~15K transactions/day",
        },
    },
    "ALT-002": {
        "id": "ALT-002",
        "severity": "critical",
        "title": "PAN Detected in Transaction Log",
        "description": "Full card number found in plaintext in settlement log file",
        "timestamp": "2026-01-05T08:45:00Z",
        "entity_id": "MID-4521",
        "regulation": "PCI-DSS Requirement 3.4",
        "status": "open",
        "evidence": """Log Entry:
2026-01-05 08:45:22 | SETTLEMENT | 4532-1234-5678-9012 | $150.00

Issue: Full PAN visible (should be masked as 4532-XXXX-XXXX-9012)

Detection Method: Regex pattern match + Luhn validation
File: settlements_20260105.log
Line: 4,521

Card Type: Visa
Issuing Country: United States""",
        "recommendations": [
            "Notify merchant's acquiring bank immediately",
            "Request log sanitization within 24 hours",
            "Verify encryption at rest for settlement files",
            "Schedule emergency PCI compliance review",
        ],
        "context": {
            "similar_violations": 3,
            "entity_name": "ElectroMart Inc",
            "entity_volume": "~15K transactions/day",
        },
    },
}

# Add default details for other alerts
for alert in alerts:
    if alert["id"] not in alert_details:
        alert_details[alert["id"]] = {
            **alert,
            "evidence": f"Alert {alert['id']} evidence details pending investigation.",
            "recommendations": [
                "Review the violation details",
                "Assign to appropriate team member",
                "Document findings",
            ],
            "context": {"similar_violations": 0, "entity_name": "N/A", "entity_volume": "N/A"},
        }

# Entities data
entities = [
    {
        "id": "BNK-1234",
        "name": "First National Bank",
        "type": "bank",
        "pci_status": "expiring",
        "pci_expiry": "2026-01-15",
        "risk_level": "high",
        "violation_count": 3,
        "country": "US",
    },
    {
        "id": "BNK-5678",
        "name": "Metro Credit Union",
        "type": "bank",
        "pci_status": "expiring",
        "pci_expiry": "2026-01-22",
        "risk_level": "medium",
        "violation_count": 1,
        "country": "US",
    },
    {
        "id": "BNK-9012",
        "name": "Pacific Trust",
        "type": "bank",
        "pci_status": "valid",
        "pci_expiry": "2026-06-30",
        "risk_level": "low",
        "violation_count": 0,
        "country": "US",
    },
    {
        "id": "MID-4521",
        "name": "ElectroMart Inc",
        "type": "merchant",
        "pci_status": "valid",
        "pci_expiry": "2026-03-15",
        "risk_level": "high",
        "violation_count": 5,
        "country": "US",
    },
    {
        "id": "MID-7890",
        "name": "QuickPay Solutions",
        "type": "merchant",
        "pci_status": "valid",
        "pci_expiry": "2026-05-20",
        "risk_level": "low",
        "violation_count": 0,
        "country": "CA",
    },
    {
        "id": "VND-456",
        "name": "SecureGate Processing",
        "type": "vendor",
        "pci_status": "valid",
        "pci_expiry": "2026-04-10",
        "risk_level": "medium",
        "violation_count": 2,
        "country": "US",
    },
]
