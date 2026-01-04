"""Demo API routes for hackathon showcase"""
from fastapi import APIRouter
from datetime import datetime
import uuid

from agents.transaction_monitor import TransactionMonitor
from mock_data import alerts, alert_details

router = APIRouter(prefix="/api/demo", tags=["Demo"])

monitor = TransactionMonitor()


@router.post("/scan")
async def demo_transaction_scan(log_content: str = None):
    """
    Demo endpoint to show Agent 3 in action.
    Scans provided log content (or uses demo data) for PAN violations.
    Creates a new alert if violations found.
    """
    # Use demo log if none provided
    if not log_content:
        log_content = """
        2026-01-05 10:15:22 | SETTLEMENT | 4532-8765-4321-9876 | $250.00
        2026-01-05 10:16:15 | AUTH | ****-****-****-1234 | $175.00
        2026-01-05 10:17:33 | REFUND | Normal refund note | $50.00
        """
    
    # Run the scan
    result = monitor.scan_transaction_log(log_content)
    
    # If violations found, create a new alert
    if result["violations"]:
        new_alert_id = f"ALT-{str(uuid.uuid4())[:4].upper()}"
        
        new_alert = {
            "id": new_alert_id,
            "severity": "critical",
            "title": f"[DEMO] PAN Detected by Agent 3",
            "description": f"Full card number found in transaction log - detected by live scan",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "entity_id": "MID-DEMO",
            "regulation": "PCI-DSS 3.4",
            "status": "open",
        }
        
        new_alert_detail = {
            **new_alert,
            "evidence": f"""Live Scan Result:

Agent: Transaction Monitor (Agent 3)
Scan Time: {result['scanned_at']}
Violations Found: {result['violations_found']}

Details:
""" + "\n".join([
                f"- {v['card_type']} card: {v['matched_pattern']}"
                for v in result['violations']
            ]),
            "recommendations": [
                "Immediately investigate source of plaintext PAN",
                "Identify and notify affected parties",
                "Implement encryption for transaction logs",
                "Conduct PCI compliance review",
            ],
            "context": {
                "similar_violations": len(alerts),
                "entity_name": "Demo Merchant",
                "entity_volume": "Demo scan",
            },
        }
        
        # Add to mock data
        alerts.insert(0, new_alert)
        alert_details[new_alert_id] = new_alert_detail
        
        return {
            "data": {
                "scan_result": result,
                "alert_created": new_alert,
                "message": f"⚠️ Violation detected! Alert {new_alert_id} created.",
            }
        }
    
    return {
        "data": {
            "scan_result": result,
            "alert_created": None,
            "message": "✅ No violations detected.",
        }
    }


@router.post("/validate-card")
async def validate_card_number(card_number: str):
    """
    Demo endpoint to validate a card number.
    Shows Luhn algorithm and card type detection.
    """
    is_valid = monitor.luhn_check(card_number)
    card_type = monitor.detect_card_type(card_number) if is_valid else None
    masked = monitor.mask_pan(card_number)
    
    return {
        "data": {
            "masked_number": masked,
            "is_valid_luhn": is_valid,
            "card_type": card_type,
            "would_trigger_alert": is_valid,
        }
    }
