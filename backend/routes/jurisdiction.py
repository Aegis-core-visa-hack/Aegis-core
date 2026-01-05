"""
Agent 4 API Routes: Cross-Jurisdiction Analyzer
Endpoints for analyzing cross-border compliance requirements
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from agents.cross_jurisdiction import CrossJurisdictionAnalyzer

router = APIRouter(prefix="/api/jurisdiction", tags=["jurisdiction"])

# Initialize the analyzer
analyzer = CrossJurisdictionAnalyzer()


# Request/Response Models
class TransactionAnalysisRequest(BaseModel):
    """Request model for transaction analysis"""
    id: Optional[str] = None
    origin_country: str
    processor_country: str
    settlement_country: str
    card_issuing_country: Optional[str] = None
    merchant_country: Optional[str] = None
    data_types: Optional[list[str]] = None


class DataFlowRequest(BaseModel):
    """Request model for data flow check"""
    origin: str
    destination: str


@router.post("/analyze")
def analyze_transaction(request: TransactionAnalysisRequest):
    """
    Analyze cross-jurisdiction compliance for a transaction.
    
    Identifies all applicable regulations, data localization requirements,
    conflicts, and provides compliance guidance.
    """
    try:
        result = analyzer.analyze_transaction(request.model_dump())
        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/check-data-flow")
def check_data_flow(origin: str, destination: str):
    """
    Check if data can legally flow between two jurisdictions.
    
    Returns requirements and warnings for the data transfer.
    
    Example: /api/jurisdiction/check-data-flow?origin=DE&destination=US
    """
    if not origin or not destination:
        raise HTTPException(status_code=400, detail="Both origin and destination are required")
    
    result = analyzer.check_data_flow_compliance(origin.upper(), destination.upper())
    return {
        "status": "success",
        "data": result
    }


@router.get("/conflicts")
def get_known_conflicts():
    """
    List all known regulatory conflicts between jurisdictions.
    
    Returns conflict types, involved regulations, and resolutions.
    """
    conflicts = analyzer.get_all_known_conflicts()
    return {
        "status": "success",
        "count": len(conflicts),
        "data": conflicts
    }


@router.get("/summary/{country_code}")
def get_jurisdiction_summary(country_code: str):
    """
    Get summary of a jurisdiction's regulatory landscape.
    
    Includes applicable regulations, data localization requirements,
    and EU adequacy status.
    """
    result = analyzer.get_jurisdiction_summary(country_code.upper())
    return {
        "status": "success",
        "data": result
    }


@router.get("/regions")
def list_supported_regions():
    """
    List all supported regulatory regions and their regulations.
    """
    return {
        "status": "success",
        "data": {
            "regions": analyzer.JURISDICTION_REGS,
            "data_localization_countries": list(analyzer.DATA_LOCALIZATION.keys()),
            "eu_adequacy_countries": analyzer.EU_ADEQUACY
        }
    }


# Demo endpoint for quick testing
@router.get("/demo")
def demo_analysis():
    """
    Run a demo analysis with a sample cross-border transaction.
    
    Transaction: German cardholder → Singapore merchant → US settlement
    """
    sample_transaction = {
        "id": "TXN-DEMO-001",
        "origin_country": "DE",
        "processor_country": "SG", 
        "settlement_country": "US",
        "card_issuing_country": "DE",
        "merchant_country": "SG"
    }
    
    result = analyzer.analyze_transaction(sample_transaction)
    return {
        "status": "success",
        "message": "Demo: German cardholder → Singapore merchant → US settlement",
        "data": result
    }
