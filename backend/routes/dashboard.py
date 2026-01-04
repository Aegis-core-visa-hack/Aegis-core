"""Dashboard API routes"""
from fastapi import APIRouter

from mock_data import dashboard_summary, agents, risk_heatmap, alerts

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/summary")
async def get_dashboard_summary():
    """Get the 4 main summary cards for dashboard"""
    return {"data": dashboard_summary}


@router.get("/risk-heatmap")
async def get_risk_heatmap():
    """Get risk levels by regulation category"""
    return {"data": {"regulations": risk_heatmap}}


@router.get("/recent-alerts")
async def get_recent_alerts(limit: int = 10):
    """Get recent alerts/notifications"""
    recent = alerts[:limit]
    unread = sum(1 for a in recent if a["status"] == "open")
    return {"data": {"alerts": recent, "unread_count": unread}}


@router.get("/agent-activity")
async def get_agent_activity():
    """Get status and recent activity of all agents"""
    running = sum(1 for a in agents if a["status"] == "running")
    return {
        "data": {
            "agents": agents,
            "summary": {
                "total": len(agents),
                "running": running,
                "idle": len(agents) - running,
                "error": 0,
            },
        }
    }
