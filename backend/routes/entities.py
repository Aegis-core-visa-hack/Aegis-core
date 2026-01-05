"""Entities API routes - Extended with Agent 2 (Ecosystem Tracker)"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from pydantic import BaseModel

from mock_data import entities, alerts
from agents.ecosystem_tracker import EcosystemTracker

router = APIRouter(prefix="/api/entities", tags=["Entities"])

# Initialize Agent 2
ecosystem_tracker = EcosystemTracker()


# Request models
class RiskCalculationRequest(BaseModel):
    violation_count: int = 0
    has_anomalies: bool = False


class StatusUpdateRequest(BaseModel):
    new_status: str


@router.get("")
async def list_entities(
    type: Optional[str] = None,
    risk_level: Optional[str] = None,
    pci_status: Optional[str] = None,
):
    """List all entities (banks, merchants, vendors) with optional filters"""
    filtered = entities
    
    if type:
        filtered = [e for e in filtered if e["type"] == type]
    
    if risk_level:
        filtered = [e for e in filtered if e["risk_level"] == risk_level]
    
    if pci_status:
        filtered = [e for e in filtered if e["pci_status"] == pci_status]
    
    return {"data": filtered}


@router.get("/expiring")
async def get_expiring_certifications(days: int = Query(default=30, ge=1, le=365)):
    """
    Get all entities with certifications expiring within N days
    Agent 2: Ecosystem Tracker functionality
    """
    expiring = ecosystem_tracker.check_expiring_certifications(days)
    return {
        "data": expiring,
        "count": len(expiring),
        "days_ahead": days
    }


@router.get("/daily-check")
async def run_daily_check():
    """
    Trigger Agent 2 daily compliance check
    Returns summary of entities checked and issues found
    """
    result = ecosystem_tracker.execute_daily_check()
    return {"data": result}


@router.get("/{entity_id}")
async def get_entity_detail(entity_id: str):
    """Get entity detail with associated violations"""
    entity = next((e for e in entities if e["id"] == entity_id), None)
    
    if not entity:
        raise HTTPException(status_code=404, detail=f"Entity {entity_id} not found")
    
    # Get violations for this entity
    entity_violations = [a for a in alerts if a.get("entity_id") == entity_id]
    
    return {
        "data": {
            **entity,
            "violations": entity_violations,
        }
    }


@router.get("/{entity_id}/certifications")
async def get_entity_certifications(entity_id: str):
    """
    Get all certifications for an entity
    Agent 2: Ecosystem Tracker functionality
    """
    cert_data = ecosystem_tracker.get_entity_certifications(entity_id)
    
    if not cert_data:
        raise HTTPException(status_code=404, detail=f"No certification data for {entity_id}")
    
    return {"data": cert_data}


@router.get("/{entity_id}/risk")
async def get_entity_risk(
    entity_id: str,
    violation_count: int = Query(default=0, ge=0),
    has_anomalies: bool = Query(default=False)
):
    """
    Calculate comprehensive risk score for an entity
    Agent 2: Ecosystem Tracker functionality
    """
    # Get entity to verify it exists
    entity = next((e for e in entities if e["id"] == entity_id), None)
    
    # Use entity's violation count if not specified
    if entity and violation_count == 0:
        violation_count = entity.get("violation_count", 0)
    
    risk_data = ecosystem_tracker.calculate_entity_risk(
        entity_id, 
        violation_count=violation_count,
        has_anomalies=has_anomalies
    )
    
    return {"data": risk_data}


@router.post("/{entity_id}/send-reminder")
async def send_reminder(entity_id: str, days_remaining: int = Query(default=30, ge=1)):
    """
    Send compliance reminder notification (demo - returns what would be sent)
    Agent 2: Ecosystem Tracker functionality
    """
    reminder = ecosystem_tracker.generate_reminder(entity_id, days_remaining)
    
    if "error" in reminder:
        raise HTTPException(status_code=404, detail=reminder["error"])
    
    return {
        "data": reminder,
        "message": "Reminder generated (demo mode - not actually sent)"
    }


@router.post("/{entity_id}/update-status")
async def update_entity_status(entity_id: str, request: StatusUpdateRequest):
    """
    Update compliance status of an entity (demo - doesn't persist)
    Agent 2: Ecosystem Tracker functionality
    """
    result = ecosystem_tracker.update_compliance_status(entity_id, request.new_status)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return {"data": result}
