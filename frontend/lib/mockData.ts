// Mock data for AEGIS dashboard - use if backend not ready

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
        severity: "critical" as const,
        title: "Transaction anomaly detected",
        description: "Unusual volume spike from Merchant MID-4521",
        timestamp: "2026-01-05T09:14:00Z",
        entity_id: "MID-4521",
        regulation: "PCI-DSS",
        status: "open"
    },
    {
        id: "ALT-002",
        severity: "critical" as const,
        title: "PAN detected in settlement log",
        description: "Full card number found in plaintext",
        timestamp: "2026-01-05T08:45:00Z",
        entity_id: "MID-4521",
        regulation: "PCI-DSS 3.4",
        status: "open"
    },
    {
        id: "ALT-003",
        severity: "high" as const,
        title: "Bank certification expiring",
        description: "BNK-123 PCI certification expires in 5 days",
        timestamp: "2026-01-05T08:30:00Z",
        entity_id: "BNK-123",
        regulation: "PCI-DSS",
        status: "open"
    },
    {
        id: "ALT-004",
        severity: "medium" as const,
        title: "GDPR amendment published",
        description: "New data retention requirements - impact analysis pending",
        timestamp: "2026-01-05T07:15:00Z",
        entity_id: null,
        regulation: "GDPR",
        status: "investigating"
    },
    {
        id: "ALT-005",
        severity: "low" as const,
        title: "Vendor assessment due",
        description: "Annual review for VND-456 due in 30 days",
        timestamp: "2026-01-05T06:00:00Z",
        entity_id: "VND-456",
        regulation: "PCI-DSS",
        status: "open"
    }
];

export const mockRiskHeatmap = [
    { name: "PCI-DSS", risk_level: "high" as const, violation_count: 12 },
    { name: "GDPR", risk_level: "medium" as const, violation_count: 8 },
    { name: "RBI", risk_level: "medium" as const, violation_count: 3 },
    { name: "CCPA", risk_level: "low" as const, violation_count: 0 },
    { name: "LGPD", risk_level: "low" as const, violation_count: 0 },
];

export const mockEntities = [
    { id: "BNK-1234", name: "First National Bank", type: "bank" as const, pci_status: "expiring" as const, pci_expiry: "2026-01-15", risk_level: "high" as const, violation_count: 3 },
    { id: "BNK-5678", name: "Metro Credit Union", type: "bank" as const, pci_status: "expiring" as const, pci_expiry: "2026-01-22", risk_level: "medium" as const, violation_count: 1 },
    { id: "BNK-9012", name: "Pacific Trust", type: "bank" as const, pci_status: "valid" as const, pci_expiry: "2026-06-30", risk_level: "low" as const, violation_count: 0 },
    { id: "MID-4521", name: "ElectroMart Inc", type: "merchant" as const, pci_status: "valid" as const, pci_expiry: "2026-03-15", risk_level: "high" as const, violation_count: 5 },
    { id: "MID-7890", name: "QuickPay Solutions", type: "merchant" as const, pci_status: "valid" as const, pci_expiry: "2026-05-20", risk_level: "low" as const, violation_count: 0 },
    { id: "VND-456", name: "SecureGate Processing", type: "vendor" as const, pci_status: "valid" as const, pci_expiry: "2026-04-10", risk_level: "medium" as const, violation_count: 2 },
];

export const mockAlertDetail = {
    id: "ALT-002",
    severity: "critical" as const,
    title: "PAN Detected in Transaction Log",
    description: "Full card number found in plaintext in settlement log file",
    timestamp: "2026-01-05T08:45:00Z",
    entity_id: "MID-4521",
    regulation: "PCI-DSS Requirement 3.4",
    status: "open" as const,
    evidence: `Log Entry:
2026-01-05 08:45:22 | SETTLEMENT | 4532-1234-5678-9012 | $150.00

Issue: Full PAN visible (should be masked as 4532-XXXX-XXXX-9012)`,
    recommendations: [
        "Notify merchant's acquiring bank immediately",
        "Request log sanitization within 24 hours",
        "Verify encryption at rest for settlement files",
        "Schedule emergency PCI compliance review"
    ],
    context: {
        similar_violations: 3,
        entity_name: "ElectroMart Inc",
        entity_volume: "~15K transactions/day"
    }
};

export const mockChatResponse = (query: string) => ({
    response: `Based on your query "${query}", here's what I found:

**Summary:** I've analyzed the current compliance landscape and found the following insights.

### Key Findings

| Metric | Value | Trend |
|--------|-------|-------|
| Total Violations | 23 | ↑ +8 this week |
| Critical Issues | 3 | Requires immediate attention |
| At-Risk Entities | 12 | 5 banks, 7 merchants |

### Recommendations
1. Prioritize the 3 critical alerts in the queue
2. Follow up on expiring certifications
3. Schedule compliance review for high-risk entities

Would you like me to generate a detailed report or take any specific action?`,
    suggested_actions: ["Generate Report", "Send Reminders", "View Details"]
});

// Type definitions
export type Alert = typeof mockAlerts[0];
export type Entity = typeof mockEntities[0];
export type RiskLevel = 'high' | 'medium' | 'low';
export type Severity = 'critical' | 'high' | 'medium' | 'low';
