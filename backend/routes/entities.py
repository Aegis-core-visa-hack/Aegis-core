"""Entities API routes"""
from fastapi import APIRouter, HTTPException
from typing import Optional

from mock_data import entities, alerts

router = APIRouter(prefix="/api/entities", tags=["Entities"])


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
