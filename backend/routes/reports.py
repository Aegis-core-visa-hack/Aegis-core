"""
AEGIS Agent 5 Routes - Evidence & Reporting API
================================================
Endpoints for generating reports, evidence packages, and managing GRC cases.
"""
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from agents.evidence_engine import evidence_engine


router = APIRouter(prefix="/api/reports", tags=["reports"])


# ============= Request Models =============

class EvidencePackageRequest(BaseModel):
    scope: str = "full"  # "full", "pci", "gdpr", "entity"
    timeframe_start: Optional[str] = None
    timeframe_end: Optional[str] = None
    entity_id: Optional[str] = None


class ReportRequest(BaseModel):
    framework: str  # "PCI-DSS", "GDPR", "SOC2", "RBI"
    region: Optional[str] = None
    timeframe_start: Optional[str] = None
    timeframe_end: Optional[str] = None


class GRCCaseRequest(BaseModel):
    title: str
    description: str
    priority: str = "medium"  # "critical", "high", "medium", "low"
    assigned_to: Optional[str] = None
    linked_violation_id: Optional[str] = None
    linked_entity_id: Optional[str] = None


class CaseStatusUpdate(BaseModel):
    status: str  # "investigating", "in_progress", "pending_review", "completed", "reopened"
    notes: Optional[str] = None
    evidence: Optional[str] = None
    actor: str = "analyst@visa.com"


class ExportRequest(BaseModel):
    data_type: str  # "violations", "cases", "entities", "reports"
    format: str = "json"  # "json", "csv"


# ============= Evidence Package Endpoints =============

@router.post("/evidence")
async def create_evidence_package(request: EvidencePackageRequest):
    """Compile an audit-ready evidence package."""
    result = evidence_engine.compile_evidence_package(
        scope=request.scope,
        timeframe_start=request.timeframe_start,
        timeframe_end=request.timeframe_end,
        entity_id=request.entity_id
    )
    return result


@router.get("/evidence/{package_id}")
async def get_evidence_package(package_id: str):
    """Get evidence package details by ID."""
    package = evidence_engine.evidence_packages.get(package_id)
    if not package:
        raise HTTPException(status_code=404, detail=f"Evidence package {package_id} not found")
    return package


# ============= Regulatory Report Endpoints =============

@router.post("/generate")
async def generate_report(request: ReportRequest):
    """Generate a regulatory compliance report."""
    result = evidence_engine.generate_regulatory_report(
        framework=request.framework,
        region=request.region,
        timeframe_start=request.timeframe_start,
        timeframe_end=request.timeframe_end
    )
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@router.get("/")
async def list_reports(
    framework: Optional[str] = Query(None, description="Filter by framework"),
    report_type: str = Query("all", description="Type: reports, evidence, or all")
):
    """List all generated reports and evidence packages."""
    reports = evidence_engine.list_reports(framework=framework, report_type=report_type)
    return {
        "reports": reports,
        "count": len(reports)
    }


# ============= GRC Case Endpoints (before dynamic routes) =============

@router.post("/cases")
async def create_grc_case(request: GRCCaseRequest):
    """Create a new GRC (Governance, Risk, Compliance) case."""
    result = evidence_engine.create_grc_case(
        title=request.title,
        description=request.description,
        priority=request.priority,
        assigned_to=request.assigned_to,
        linked_violation_id=request.linked_violation_id,
        linked_entity_id=request.linked_entity_id
    )
    return result


@router.get("/cases")
async def list_grc_cases(
    status: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    assigned_to: Optional[str] = Query(None, description="Filter by assignee")
):
    """List all GRC cases with optional filters."""
    cases = evidence_engine.list_grc_cases(
        status=status,
        priority=priority,
        assigned_to=assigned_to
    )
    return {
        "cases": cases,
        "count": len(cases)
    }


@router.get("/cases/summary")
async def get_remediation_summary():
    """Get a summary of all remediation cases."""
    return evidence_engine.get_remediation_summary()


@router.get("/cases/{case_id}")
async def get_grc_case(case_id: str):
    """Get GRC case details by ID."""
    case = evidence_engine.get_grc_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail=f"Case {case_id} not found")
    return case


@router.patch("/cases/{case_id}")
async def update_case_status(case_id: str, request: CaseStatusUpdate):
    """Update the status of a GRC case."""
    result = evidence_engine.update_remediation_status(
        case_id=case_id,
        status=request.status,
        notes=request.notes,
        evidence=request.evidence,
        actor=request.actor
    )
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


# ============= Framework Templates (before dynamic routes) =============

@router.get("/frameworks")
async def list_frameworks():
    """List available report frameworks and templates."""
    templates = evidence_engine.report_templates
    return {
        "frameworks": [
            {
                "id": key,
                "title": val["title"],
                "sections": val["sections"],
                "requirements_count": val["requirements_count"]
            }
            for key, val in templates.items()
        ]
    }


# ============= Dynamic Report Routes (MUST be last) =============

@router.get("/{report_id}")
async def get_report_detail(report_id: str):
    """Get report details by ID."""
    report = evidence_engine.get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail=f"Report {report_id} not found")
    return report


@router.get("/{report_id}/download")
async def download_report(report_id: str):
    """Download a report (mock - returns metadata)."""
    report = evidence_engine.get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail=f"Report {report_id} not found")
    
    return {
        "message": "Download initiated",
        "report_id": report_id,
        "filename": f"{report_id}.pdf",
        "size_bytes": report.get("size_bytes", 0),
        "status": "In production, this would return a file download"
    }


# ============= Export Endpoints =============

@router.post("/export")
async def export_data(request: ExportRequest):
    """Export data in various formats."""
    result = evidence_engine.export_data(
        data_type=request.data_type,
        format=request.format
    )
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result
