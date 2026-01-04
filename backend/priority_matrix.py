"""2D Heatmap data for priority matrix - Criticality × Due Date"""
from datetime import datetime, timedelta

# Generate 2D priority matrix data from alerts and entities
def get_priority_matrix():
    """
    Creates a 2D matrix view:
    - X-axis: Due Date (Overdue, This Week, This Month, Later)
    - Y-axis: Criticality (Critical, High, Medium, Low)
    
    Each cell contains items that fall into that category.
    """
    # Sample issues for the matrix
    issues = [
        # Critical + Overdue
        {"id": "ALT-001", "title": "Transaction anomaly", "entity": "MID-4521", "severity": "critical", "due": "overdue", "due_date": "2026-01-03"},
        {"id": "ALT-002", "title": "PAN in settlement log", "entity": "MID-4521", "severity": "critical", "due": "this_week", "due_date": "2026-01-08"},
        
        # High priority
        {"id": "ALT-003", "title": "Bank cert expiring", "entity": "BNK-1234", "severity": "high", "due": "this_week", "due_date": "2026-01-10"},
        {"id": "ISS-001", "title": "GDPR consent update", "entity": "BNK-5678", "severity": "high", "due": "this_month", "due_date": "2026-01-25"},
        
        # Medium priority
        {"id": "ISS-002", "title": "Vendor reassessment", "entity": "VND-456", "severity": "medium", "due": "this_month", "due_date": "2026-01-20"},
        {"id": "ISS-003", "title": "Policy document update", "entity": None, "severity": "medium", "due": "later", "due_date": "2026-02-15"},
        {"id": "ALT-004", "title": "GDPR amendment review", "entity": None, "severity": "medium", "due": "this_week", "due_date": "2026-01-09"},
        
        # Low priority
        {"id": "ISS-004", "title": "Training renewal", "entity": "BNK-9012", "severity": "low", "due": "later", "due_date": "2026-03-01"},
        {"id": "ISS-005", "title": "Annual audit prep", "entity": None, "severity": "low", "due": "this_month", "due_date": "2026-01-28"},
    ]
    
    # Build matrix structure
    matrix = {
        "critical": {"overdue": [], "this_week": [], "this_month": [], "later": []},
        "high": {"overdue": [], "this_week": [], "this_month": [], "later": []},
        "medium": {"overdue": [], "this_week": [], "this_month": [], "later": []},
        "low": {"overdue": [], "this_week": [], "this_month": [], "later": []},
    }
    
    # Populate matrix
    for issue in issues:
        severity = issue["severity"]
        due = issue["due"]
        matrix[severity][due].append(issue)
    
    # Calculate summary counts
    summary = {
        "total_issues": len(issues),
        "overdue": sum(1 for i in issues if i["due"] == "overdue"),
        "critical_overdue": len(matrix["critical"]["overdue"]),
        "needs_attention": sum(1 for i in issues if i["due"] in ["overdue", "this_week"] and i["severity"] in ["critical", "high"]),
    }
    
    return {
        "matrix": matrix,
        "summary": summary,
        "last_updated": datetime.now().isoformat(),
    }


# Standalone data for import
priority_matrix_data = get_priority_matrix()
