"""
Agent 2: Ecosystem Compliance Tracker
Tracks compliance status of member banks, merchants, and vendors.
Monitors certifications, identifies at-risk entities, and triggers alerts.
"""
from datetime import datetime, date, timedelta
from typing import Optional, List, Dict, Any


# Certification data for entities (extends mock_data)
ENTITY_CERTIFICATIONS = {
    "BNK-1234": {
        "certifications": [
            {"type": "PCI-DSS", "level": "Level 1", "expiry": "2026-01-15", "status": "expiring", "last_assessment": "2025-01-15"},
            {"type": "SOC2", "expiry": "2026-08-01", "status": "valid", "last_assessment": "2025-08-01"}
        ],
        "contact_email": "compliance@firstnational.com",
        "relationship_manager": "David Chen"
    },
    "BNK-5678": {
        "certifications": [
            {"type": "PCI-DSS", "level": "Level 1", "expiry": "2026-01-22", "status": "expiring", "last_assessment": "2025-01-22"},
            {"type": "ISO-27001", "expiry": "2026-09-15", "status": "valid", "last_assessment": "2025-09-15"}
        ],
        "contact_email": "security@metrocu.com",
        "relationship_manager": "Sarah Mills"
    },
    "BNK-9012": {
        "certifications": [
            {"type": "PCI-DSS", "level": "Level 1", "expiry": "2026-06-30", "status": "valid", "last_assessment": "2025-06-30"},
            {"type": "SOC2", "expiry": "2026-07-15", "status": "valid", "last_assessment": "2025-07-15"}
        ],
        "contact_email": "compliance@pacifictrust.com",
        "relationship_manager": "Michael Wong"
    },
    "MID-4521": {
        "certifications": [
            {"type": "PCI-DSS", "level": "SAQ-A", "expiry": "2026-03-15", "status": "valid", "last_assessment": "2025-03-15"}
        ],
        "contact_email": "security@electromart.com",
        "relationship_manager": "Lisa Park",
        "sponsoring_bank": "BNK-1234"
    },
    "MID-7890": {
        "certifications": [
            {"type": "PCI-DSS", "level": "SAQ-A", "expiry": "2026-05-20", "status": "valid", "last_assessment": "2025-05-20"}
        ],
        "contact_email": "compliance@quickpay.ca",
        "relationship_manager": "James Wilson",
        "sponsoring_bank": "BNK-9012"
    },
    "VND-456": {
        "certifications": [
            {"type": "PCI-DSS", "level": "Service Provider", "expiry": "2026-04-10", "status": "valid", "last_assessment": "2025-04-10"},
            {"type": "SOC2", "expiry": "2026-05-01", "status": "valid", "last_assessment": "2025-05-01"}
        ],
        "contact_email": "audit@securegate.com",
        "relationship_manager": "Emily Chen"
    }
}

# Notification thresholds (days before expiry)
NOTIFICATION_THRESHOLDS = [90, 60, 30, 14, 7]

# Risk weights for scoring
RISK_WEIGHTS = {
    "certification": 30,  # Max 30 points
    "violations": 30,     # Max 30 points
    "anomalies": 20,      # Max 20 points
    "jurisdiction": 10,   # Max 10 points
    "relationship": 10    # Max 10 points (for merchants)
}


class EcosystemTracker:
    """Track compliance status of ecosystem entities"""

    def __init__(self):
        self.notification_thresholds = NOTIFICATION_THRESHOLDS
        self.risk_weights = RISK_WEIGHTS

    def get_entity_certifications(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """
        Get all certifications for an entity
        Returns: {entity_id, certifications[], contact_email}
        """
        cert_data = ENTITY_CERTIFICATIONS.get(entity_id)
        if not cert_data:
            return None

        # Calculate days remaining for each certification
        today = date.today()
        certs_with_days = []
        
        for cert in cert_data.get("certifications", []):
            expiry_date = datetime.strptime(cert["expiry"], "%Y-%m-%d").date()
            days_remaining = (expiry_date - today).days
            
            # Determine current status based on days remaining
            if days_remaining < 0:
                status = "expired"
            elif days_remaining <= 30:
                status = "expiring"
            else:
                status = "valid"
            
            certs_with_days.append({
                **cert,
                "days_remaining": days_remaining,
                "status": status
            })

        return {
            "entity_id": entity_id,
            "certifications": certs_with_days,
            "contact_email": cert_data.get("contact_email"),
            "relationship_manager": cert_data.get("relationship_manager"),
            "sponsoring_bank": cert_data.get("sponsoring_bank")
        }

    def check_expiring_certifications(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        Find all entities with certifications expiring within N days
        Returns: [{entity_id, cert_type, expiry_date, days_remaining, risk_level}]
        """
        today = date.today()
        expiring = []

        for entity_id, cert_data in ENTITY_CERTIFICATIONS.items():
            for cert in cert_data.get("certifications", []):
                expiry_date = datetime.strptime(cert["expiry"], "%Y-%m-%d").date()
                days_remaining = (expiry_date - today).days
                
                # Include if expiring within the specified days and not already expired
                if 0 <= days_remaining <= days:
                    # Determine risk level based on days remaining
                    if days_remaining <= 7:
                        risk_level = "critical"
                    elif days_remaining <= 14:
                        risk_level = "high"
                    elif days_remaining <= 30:
                        risk_level = "medium"
                    else:
                        risk_level = "low"

                    expiring.append({
                        "entity_id": entity_id,
                        "entity_type": self._get_entity_type(entity_id),
                        "cert_type": cert["type"],
                        "cert_level": cert.get("level"),
                        "expiry_date": cert["expiry"],
                        "days_remaining": days_remaining,
                        "risk_level": risk_level,
                        "contact_email": cert_data.get("contact_email"),
                        "relationship_manager": cert_data.get("relationship_manager")
                    })

        # Sort by days remaining (most urgent first)
        expiring.sort(key=lambda x: x["days_remaining"])
        return expiring

    def calculate_entity_risk(self, entity_id: str, violation_count: int = 0, 
                               has_anomalies: bool = False) -> Dict[str, Any]:
        """
        Calculate comprehensive risk score for an entity
        Risk score is 0-100, calculated from multiple factors
        """
        cert_data = ENTITY_CERTIFICATIONS.get(entity_id)
        if not cert_data:
            return {
                "risk_score": 0,
                "risk_level": "unknown",
                "factors": {},
                "top_concerns": ["Entity not found in system"]
            }

        today = date.today()
        factors = {}
        top_concerns = []

        # 1. CERTIFICATION FACTOR (0-30 points)
        min_days_remaining = float('inf')
        for cert in cert_data.get("certifications", []):
            expiry_date = datetime.strptime(cert["expiry"], "%Y-%m-%d").date()
            days_remaining = (expiry_date - today).days
            min_days_remaining = min(min_days_remaining, days_remaining)

        if min_days_remaining < 0:
            factors["certification"] = 30
            top_concerns.append(f"Certification expired {abs(min_days_remaining)} days ago")
        elif min_days_remaining <= 30:
            factors["certification"] = 25
            top_concerns.append(f"Certification expires in {min_days_remaining} days")
        elif min_days_remaining <= 60:
            factors["certification"] = 15
            top_concerns.append(f"Certification expires in {min_days_remaining} days")
        elif min_days_remaining <= 90:
            factors["certification"] = 5
        else:
            factors["certification"] = 0

        # 2. VIOLATION HISTORY (0-30 points)
        if violation_count == 0:
            factors["violations"] = 0
        elif violation_count <= 2:
            factors["violations"] = 5
        elif violation_count <= 4:
            factors["violations"] = 15
            top_concerns.append(f"{violation_count} unresolved violations")
        else:
            factors["violations"] = 30
            top_concerns.append(f"{violation_count} critical violation count")

        # 3. TRANSACTION ANOMALY FACTOR (0-20 points)
        if has_anomalies:
            factors["anomalies"] = 20
            top_concerns.append("Transaction anomalies detected")
        else:
            factors["anomalies"] = 0

        # 4. JURISDICTION FACTOR (0-10 points) - simplified for demo
        factors["jurisdiction"] = 0  # Would check entity country against high-risk list

        # 5. RELATIONSHIP FACTOR (0-10 points) - for merchants
        sponsoring_bank = cert_data.get("sponsoring_bank")
        if sponsoring_bank:
            # Check sponsoring bank's compliance status
            bank_cert_data = ENTITY_CERTIFICATIONS.get(sponsoring_bank)
            if bank_cert_data:
                for cert in bank_cert_data.get("certifications", []):
                    if cert["type"] == "PCI-DSS":
                        expiry_date = datetime.strptime(cert["expiry"], "%Y-%m-%d").date()
                        bank_days = (expiry_date - today).days
                        if bank_days < 0:
                            factors["relationship"] = 10
                            top_concerns.append(f"Sponsoring bank {sponsoring_bank} non-compliant")
                        elif bank_days <= 30:
                            factors["relationship"] = 5
                        else:
                            factors["relationship"] = 0
                        break
            else:
                factors["relationship"] = 0
        else:
            factors["relationship"] = 0

        # Calculate total risk score
        total_score = sum(factors.values())
        
        # Determine risk level
        if total_score >= 76:
            risk_level = "critical"
        elif total_score >= 51:
            risk_level = "high"
        elif total_score >= 26:
            risk_level = "medium"
        else:
            risk_level = "low"

        return {
            "entity_id": entity_id,
            "risk_score": total_score,
            "risk_level": risk_level,
            "factors": factors,
            "top_concerns": top_concerns if top_concerns else ["No immediate concerns"]
        }

    def generate_reminder(self, entity_id: str, days_remaining: int) -> Dict[str, Any]:
        """
        Generate compliance reminder notification
        Returns: {notification_id, recipient, subject, body, urgency}
        """
        cert_data = ENTITY_CERTIFICATIONS.get(entity_id)
        if not cert_data:
            return {"error": "Entity not found"}

        # Determine urgency level
        if days_remaining > 60:
            urgency = "standard"
        elif days_remaining > 30:
            urgency = "elevated"
        elif days_remaining > 14:
            urgency = "urgent"
        else:
            urgency = "critical"

        entity_type = self._get_entity_type(entity_id)
        recipient = cert_data.get("contact_email", "unknown@example.com")
        
        # Generate notification content
        subject = f"[{urgency.upper()}] PCI Certification Expiring - Action Required"
        
        body = f"""Dear Compliance Team,

Your PCI-DSS certification is expiring in {days_remaining} days.

Entity: {entity_id}
Entity Type: {entity_type.title()}
Days Remaining: {days_remaining}

Required Action:
• Schedule renewal assessment
• Complete SAQ documentation  
• Submit to acquiring bank

Failure to renew may result in:
• Transaction processing restrictions
• Increased liability for fraud
• Regulatory penalties

Contact your relationship manager ({cert_data.get('relationship_manager', 'N/A')}) for assistance.

Best regards,
AEGIS Compliance Platform"""

        return {
            "notification_id": f"NTF-{entity_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "entity_id": entity_id,
            "recipient": recipient,
            "subject": subject,
            "body": body,
            "urgency": urgency,
            "channels": self._get_notification_channels(urgency),
            "sent_at": datetime.utcnow().isoformat() + "Z"
        }

    def update_compliance_status(self, entity_id: str, new_status: str) -> Dict[str, Any]:
        """
        Update the compliance status of an entity (demo - doesn't persist)
        Returns: {previous_status, new_status, changed_at}
        """
        cert_data = ENTITY_CERTIFICATIONS.get(entity_id)
        if not cert_data:
            return {"error": "Entity not found"}

        # Get current status from first PCI certification
        previous_status = "unknown"
        for cert in cert_data.get("certifications", []):
            if cert["type"] == "PCI-DSS":
                previous_status = cert.get("status", "unknown")
                break

        # Validate new status
        valid_statuses = ["compliant", "at_risk", "non_compliant", "valid", "expiring", "expired"]
        if new_status not in valid_statuses:
            return {"error": f"Invalid status. Must be one of: {valid_statuses}"}

        return {
            "entity_id": entity_id,
            "previous_status": previous_status,
            "new_status": new_status,
            "changed_at": datetime.utcnow().isoformat() + "Z",
            "audit_log_id": f"AUD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        }

    def execute_daily_check(self) -> Dict[str, Any]:
        """
        Execute daily ecosystem compliance check
        Returns summary of entities checked and issues found
        """
        entities_checked = 0
        at_risk_found = 0
        non_compliant_found = 0
        notifications_needed = 0
        
        today = date.today()
        
        for entity_id, cert_data in ENTITY_CERTIFICATIONS.items():
            entities_checked += 1
            
            for cert in cert_data.get("certifications", []):
                if cert["type"] == "PCI-DSS":
                    expiry_date = datetime.strptime(cert["expiry"], "%Y-%m-%d").date()
                    days_remaining = (expiry_date - today).days
                    
                    if days_remaining < 0:
                        non_compliant_found += 1
                    elif days_remaining <= 30:
                        at_risk_found += 1
                    
                    # Check if notification is needed
                    if days_remaining in self.notification_thresholds:
                        notifications_needed += 1
                    break

        return {
            "execution_time": datetime.utcnow().isoformat() + "Z",
            "entities_checked": entities_checked,
            "at_risk_found": at_risk_found,
            "non_compliant_found": non_compliant_found,
            "notifications_needed": notifications_needed,
            "status": "completed",
            "next_run": (datetime.utcnow() + timedelta(days=1)).isoformat() + "Z"
        }

    def _get_entity_type(self, entity_id: str) -> str:
        """Determine entity type from ID prefix"""
        if entity_id.startswith("BNK"):
            return "member_bank"
        elif entity_id.startswith("MID"):
            return "merchant"
        elif entity_id.startswith("VND"):
            return "vendor"
        return "unknown"

    def _get_notification_channels(self, urgency: str) -> List[str]:
        """Determine notification channels based on urgency"""
        channels = ["email", "in_app"]
        if urgency in ["urgent", "critical"]:
            channels.append("sms")
        if urgency == "critical":
            channels.append("phone")
        return channels


# Demo function
def demo_check():
    """Demo the ecosystem tracker"""
    tracker = EcosystemTracker()
    
    # Run daily check
    print("=== Daily Compliance Check ===")
    result = tracker.execute_daily_check()
    print(f"Result: {result}")
    
    # Check expiring certifications
    print("\n=== Expiring Certifications (30 days) ===")
    expiring = tracker.check_expiring_certifications(30)
    for e in expiring:
        print(f"  {e['entity_id']}: {e['cert_type']} expires in {e['days_remaining']} days")
    
    # Calculate risk for a high-risk entity
    print("\n=== Risk Calculation: BNK-1234 ===")
    risk = tracker.calculate_entity_risk("BNK-1234", violation_count=3, has_anomalies=False)
    print(f"  Score: {risk['risk_score']}/100 ({risk['risk_level']})")
    print(f"  Concerns: {risk['top_concerns']}")
    
    return result


if __name__ == "__main__":
    demo_check()
