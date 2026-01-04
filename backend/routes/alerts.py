"""Alerts API routes"""
from fastapi import APIRouter, HTTPException
from typing import Optional

from mock_data import alerts, alert_details

router = APIRouter(prefix="/api/alerts", tags=["Alerts"])


@router.get("")
async def list_alerts(severity: Optional[str] = None, status: Optional[str] = None):
    """List all alerts with optional filters"""
    filtered = alerts
    
    if severity:
        filtered = [a for a in filtered if a["severity"] == severity]
    
    if status:
        filtered = [a for a in filtered if a["status"] == status]
    
    return {"data": filtered}


@router.get("/{alert_id}")
async def get_alert_detail(alert_id: str):
    """Get alert detail with evidence and recommendations"""
    if alert_id not in alert_details:
        raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")
    
    return {"data": alert_details[alert_id]}


@router.patch("/{alert_id}")
async def update_alert_status(alert_id: str, status: str):
    """Update alert status (open → investigating → resolved)"""
    valid_statuses = ["open", "investigating", "resolved", "false_positive"]
    
    if status not in valid_statuses:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid status. Must be one of: {valid_statuses}"
        )
    
    if alert_id not in alert_details:
        raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")
    
    # Update in mock data
    alert_details[alert_id]["status"] = status
    
    # Also update in alerts list
    for alert in alerts:
        if alert["id"] == alert_id:
            alert["status"] = status
            break
    
    return {"data": alert_details[alert_id], "message": f"Status updated to {status}"}
