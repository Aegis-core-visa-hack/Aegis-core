"""
Agent 1: Regulatory Intelligence Monitor
Monitors regulatory sources for updates, parses changes, alerts on new regulations.
Demo implementation for hackathon - returns mock data, no actual scraping.
"""
import hashlib
from datetime import datetime
from typing import Optional


# Mock regulatory sources
MOCK_SOURCES = [
    {"id": "SRC-EU-GDPR", "name": "EU GDPR", "url": "https://eur-lex.europa.eu", "region": "EU", "method": "web"},
    {"id": "SRC-PCI", "name": "PCI Security Standards", "url": "https://pcisecuritystandards.org", "region": "Global", "method": "rss"},
    {"id": "SRC-RBI", "name": "RBI Circulars", "url": "https://rbi.org.in", "region": "IN", "method": "web"},
    {"id": "SRC-CCPA", "name": "California Consumer Privacy Act", "url": "https://oag.ca.gov", "region": "US-CA", "method": "web"},
    {"id": "SRC-MAS", "name": "MAS Technology Risk Guidelines", "url": "https://mas.gov.sg", "region": "SG", "method": "api"},
]

# Mock regulations data
MOCK_REGULATIONS = [
    {
        "id": "REG-2026-001",
        "title": "GDPR Amendment - AI Act Integration",
        "source": "europa.eu",
        "source_id": "SRC-EU-GDPR",
        "region": "EU",
        "summary": "New requirements for AI systems processing personal data under GDPR. Mandates algorithmic transparency and data subject rights for automated decision-making.",
        "effective_date": "2026-03-01",
        "published_date": "2026-01-03",
        "status": "new",
        "impact": "high",
        "affected_entities": 234,
        "obligations": [
            "Implement AI system auditing for data processing decisions",
            "Provide data subjects the right to explanation of AI decisions",
            "Maintain human oversight for high-risk AI data processing",
        ],
        "penalties": "Up to €20M or 4% of annual global turnover",
    },
    {
        "id": "REG-2026-002", 
        "title": "RBI Data Localization Update",
        "source": "rbi.org.in",
        "source_id": "SRC-RBI",
        "region": "IN",
        "summary": "Extended compliance deadline for payment data storage within India. Clarifies scope for cross-border transaction data and introduces tiered compliance.",
        "effective_date": "2026-06-30",
        "published_date": "2026-01-02",
        "status": "updated",
        "impact": "medium",
        "affected_entities": 12,
        "obligations": [
            "Store all payment system data within India",
            "Implement data mirroring for cross-border transactions",
            "Submit quarterly compliance reports to RBI",
        ],
        "penalties": "Suspension of authorization to operate",
    },
    {
        "id": "REG-2026-003",
        "title": "PCI-DSS v4.0.1 Minor Update",
        "source": "pcisecuritystandards.org",
        "source_id": "SRC-PCI",
        "region": "Global",
        "summary": "Clarification of multi-factor authentication requirements and updated guidance for cloud-based cardholder data environments.",
        "effective_date": "2026-04-01",
        "published_date": "2026-01-04",
        "status": "updated",
        "impact": "low",
        "affected_entities": 458,
        "obligations": [
            "Implement phishing-resistant MFA for all CDE access",
            "Update cloud responsibility matrices",
            "Annual targeted risk analysis for customized controls",
        ],
        "penalties": "Fines $5,000-$100,000/month + potential card brand restrictions",
    },
    {
        "id": "REG-2026-004",
        "title": "CCPA Amendment - Sensitive Data Categories",
        "source": "oag.ca.gov",
        "source_id": "SRC-CCPA",
        "region": "US-CA",
        "summary": "Expands definition of sensitive personal information to include financial account credentials and precise geolocation from payment terminals.",
        "effective_date": "2026-07-01",
        "published_date": "2026-01-01",
        "status": "new",
        "impact": "medium",
        "affected_entities": 89,
        "obligations": [
            "Update privacy notices to include new sensitive data categories",
            "Implement opt-out mechanisms for geolocation data",
            "Review third-party data sharing agreements",
        ],
        "penalties": "$2,500 per unintentional violation, $7,500 per intentional violation",
    },
]

# Entity impact mapping
ENTITY_AFFECTED_BY_REGULATION = {
    "REG-2026-001": ["BNK-1234", "BNK-5678", "MID-4521", "VND-456"],  # EU entities
    "REG-2026-002": ["BNK-9012"],  # India-connected entities
    "REG-2026-003": ["BNK-1234", "BNK-5678", "BNK-9012", "MID-4521", "MID-7890", "VND-456"],  # Global
    "REG-2026-004": ["MID-4521", "MID-7890"],  # US-CA entities
}


class RegulatoryMonitor:
    """Monitor regulatory sources and detect changes - Demo implementation"""
    
    def __init__(self):
        # Store known regulation hashes for change detection
        self.regulation_hashes: dict[str, str] = {}
        self._initialize_hashes()
    
    def _initialize_hashes(self):
        """Initialize hash cache with current regulations"""
        for reg in MOCK_REGULATIONS:
            content = f"{reg['title']}{reg['summary']}{reg['effective_date']}"
            self.regulation_hashes[reg["id"]] = hashlib.md5(content.encode()).hexdigest()
    
    def get_sources(self) -> list[dict]:
        """Return list of monitored regulatory sources"""
        return MOCK_SOURCES
    
    def fetch_source(self, source_id: str, method: str = "mock") -> dict:
        """
        Fetch content from regulatory source.
        For hackathon: Returns mock data, doesn't actually scrape.
        """
        source = next((s for s in MOCK_SOURCES if s["id"] == source_id), None)
        if not source:
            return {"error": f"Source {source_id} not found", "content": None}
        
        # Find regulations from this source
        regulations = [r for r in MOCK_REGULATIONS if r["source_id"] == source_id]
        
        return {
            "source_id": source_id,
            "source_name": source["name"],
            "fetched_at": datetime.utcnow().isoformat() + "Z",
            "method": method,
            "regulations_found": len(regulations),
            "content_hash": hashlib.md5(str(regulations).encode()).hexdigest()[:16],
        }
    
    def detect_changes(self, regulation_id: str, new_hash: str) -> bool:
        """Compare hash with stored version to detect changes"""
        stored_hash = self.regulation_hashes.get(regulation_id)
        if stored_hash is None:
            # New regulation
            self.regulation_hashes[regulation_id] = new_hash
            return True
        return stored_hash != new_hash
    
    def get_all_regulations(self, region: Optional[str] = None, status: Optional[str] = None) -> list[dict]:
        """Get all tracked regulations with optional filters"""
        result = MOCK_REGULATIONS.copy()
        
        if region:
            result = [r for r in result if r["region"].lower() == region.lower()]
        if status:
            result = [r for r in result if r["status"].lower() == status.lower()]
        
        return result
    
    def get_regulation(self, regulation_id: str) -> Optional[dict]:
        """Get full regulation details by ID"""
        return next((r for r in MOCK_REGULATIONS if r["id"] == regulation_id), None)
    
    def parse_regulation(self, content: str) -> dict:
        """
        Use LLM to extract structured obligations from regulation text.
        For hackathon: Returns mock parsed structure.
        """
        # Mock parsing - in production would use Gemini to parse
        return {
            "parsed_at": datetime.utcnow().isoformat() + "Z",
            "title": "Parsed Regulation Title",
            "summary": "AI-extracted summary of the regulation",
            "obligations": [
                "Obligation 1 extracted by AI",
                "Obligation 2 extracted by AI",
            ],
            "effective_date": "2026-06-01",
            "jurisdiction": "Unknown",
            "confidence_score": 0.87,
        }
    
    def calculate_impact(self, regulation_id: str) -> dict:
        """
        Determine affected entities for a regulation.
        Returns count and list of affected entity IDs.
        """
        regulation = self.get_regulation(regulation_id)
        if not regulation:
            return {"error": "Regulation not found", "affected_count": 0, "entity_ids": []}
        
        affected_ids = ENTITY_AFFECTED_BY_REGULATION.get(regulation_id, [])
        
        # Determine urgency based on effective date and impact
        days_until_effective = (
            datetime.fromisoformat(regulation["effective_date"]) - datetime.utcnow()
        ).days
        
        if days_until_effective < 30:
            urgency = "critical"
        elif days_until_effective < 90:
            urgency = "high"
        elif days_until_effective < 180:
            urgency = "medium"
        else:
            urgency = "low"
        
        return {
            "regulation_id": regulation_id,
            "regulation_title": regulation["title"],
            "affected_count": len(affected_ids),
            "entity_ids": affected_ids,
            "urgency": urgency,
            "days_until_effective": days_until_effective,
            "impact_level": regulation["impact"],
        }
    
    def check_for_updates(self) -> dict:
        """
        Trigger a check for regulatory updates across all sources.
        Demo: Returns simulated scan results.
        """
        scan_results = {
            "scanned_at": datetime.utcnow().isoformat() + "Z",
            "sources_checked": len(MOCK_SOURCES),
            "new_regulations": 0,
            "updated_regulations": 0,
            "unchanged": 0,
            "alerts_generated": [],
        }
        
        for source in MOCK_SOURCES:
            fetch_result = self.fetch_source(source["id"])
            # Simulate finding updates
            source_regs = [r for r in MOCK_REGULATIONS if r["source_id"] == source["id"]]
            for reg in source_regs:
                if reg["status"] == "new":
                    scan_results["new_regulations"] += 1
                    scan_results["alerts_generated"].append({
                        "type": "new_regulation",
                        "regulation_id": reg["id"],
                        "title": reg["title"],
                        "impact": reg["impact"],
                    })
                elif reg["status"] == "updated":
                    scan_results["updated_regulations"] += 1
                    scan_results["alerts_generated"].append({
                        "type": "regulation_updated",
                        "regulation_id": reg["id"],
                        "title": reg["title"],
                        "impact": reg["impact"],
                    })
                else:
                    scan_results["unchanged"] += 1
        
        return scan_results


# Demo function
def demo_regulatory_scan():
    """Demo the regulatory monitor"""
    monitor = RegulatoryMonitor()
    
    print("=== Regulatory Intelligence Monitor Demo ===\n")
    
    # List sources
    print("Monitored Sources:")
    for source in monitor.get_sources():
        print(f"  - {source['name']} ({source['region']})")
    
    print("\n--- Checking for Updates ---")
    results = monitor.check_for_updates()
    print(f"Sources checked: {results['sources_checked']}")
    print(f"New regulations: {results['new_regulations']}")
    print(f"Updated regulations: {results['updated_regulations']}")
    
    print("\n--- Regulations Found ---")
    for reg in monitor.get_all_regulations():
        print(f"  [{reg['status'].upper()}] {reg['title']} ({reg['region']})")
    
    return results


if __name__ == "__main__":
    demo_regulatory_scan()
