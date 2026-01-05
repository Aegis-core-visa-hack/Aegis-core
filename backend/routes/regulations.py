"""
API routes for Regulatory Intelligence (Agent 1)
Provides endpoints for accessing regulations, checking updates, and analyzing impact.
"""
from typing import Optional
from fastapi import APIRouter, HTTPException

from agents.regulatory_monitor import RegulatoryMonitor

router = APIRouter(prefix="/api/regulations", tags=["regulations"])

# Initialize the regulatory monitor agent
regulatory_monitor = RegulatoryMonitor()


@router.get("/")
def list_regulations(region: Optional[str] = None, status: Optional[str] = None):
    """
    List all tracked regulations with optional filters.
    
    Args:
        region: Filter by region (EU, US, IN, SG, Global, US-CA)
        status: Filter by status (new, updated, unchanged)
    
    Returns:
        List of regulations matching the filters
    """
    regulations = regulatory_monitor.get_all_regulations(region=region, status=status)
    return {
        "count": len(regulations),
        "filters": {"region": region, "status": status},
        "regulations": regulations,
    }


@router.get("/sources")
def list_sources():
    """
    List all monitored regulatory sources.
    
    Returns:
        List of regulatory sources with metadata
    """
    sources = regulatory_monitor.get_sources()
    return {
        "count": len(sources),
        "sources": sources,
    }


@router.get("/{regulation_id}")
def get_regulation(regulation_id: str):
    """
    Get full details for a specific regulation.
    
    Args:
        regulation_id: The regulation ID (e.g., REG-2026-001)
    
    Returns:
        Full regulation details including obligations and penalties
    """
    regulation = regulatory_monitor.get_regulation(regulation_id)
    if not regulation:
        raise HTTPException(status_code=404, detail=f"Regulation {regulation_id} not found")
    return regulation


@router.get("/{regulation_id}/impact")
def get_regulation_impact(regulation_id: str):
    """
    Get entities affected by a specific regulation.
    
    Args:
        regulation_id: The regulation ID
    
    Returns:
        Impact analysis including affected entities and urgency level
    """
    impact = regulatory_monitor.calculate_impact(regulation_id)
    if "error" in impact:
        raise HTTPException(status_code=404, detail=impact["error"])
    return impact


@router.post("/check-updates")
def check_for_updates():
    """
    Trigger a check for regulatory updates across all sources.
    Demo endpoint - simulates scanning regulatory sources.
    
    Returns:
        Scan results with new/updated regulations found
    """
    results = regulatory_monitor.check_for_updates()
    return results


@router.get("/summary/stats")
def get_regulation_stats():
    """
    Get summary statistics for regulations.
    
    Returns:
        Counts by status, region, and impact level
    """
    all_regs = regulatory_monitor.get_all_regulations()
    
    stats = {
        "total_regulations": len(all_regs),
        "by_status": {},
        "by_region": {},
        "by_impact": {},
        "sources_monitored": len(regulatory_monitor.get_sources()),
    }
    
    for reg in all_regs:
        # Count by status
        status = reg["status"]
        stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
        
        # Count by region
        region = reg["region"]
        stats["by_region"][region] = stats["by_region"].get(region, 0) + 1
        
        # Count by impact
        impact = reg["impact"]
        stats["by_impact"][impact] = stats["by_impact"].get(impact, 0) + 1
    
    return stats
