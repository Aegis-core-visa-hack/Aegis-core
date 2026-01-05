"""
Agent 4: Cross-Jurisdiction Analyzer
Analyzes transactions crossing multiple regulatory jurisdictions.
Identifies conflicts and provides compliance guidance.
"""
from typing import Optional
from datetime import datetime


class CrossJurisdictionAnalyzer:
    """Analyze cross-border compliance requirements"""
    
    # Jurisdiction → Applicable Regulations mapping
    JURISDICTION_REGS = {
        "EU": ["GDPR", "PSD2", "DORA"],
        "US": ["CCPA", "GLBA", "SOX"],
        "IN": ["RBI-DL", "PDPB", "IT-ACT"],
        "SG": ["PDPA", "MAS-TRM"],
        "UK": ["UK-GDPR", "FCA"],
        "JP": ["APPI"],
        "BR": ["LGPD"],
        "CN": ["PIPL", "CSL"],
        "RU": ["FZ-242"],
        "AU": ["Privacy Act"],
        "GLOBAL": ["PCI-DSS", "ISO-27001"]
    }
    
    # Countries in each regulatory region
    COUNTRY_TO_REGION = {
        # EU countries
        "DE": "EU", "FR": "EU", "IT": "EU", "ES": "EU", "NL": "EU", 
        "BE": "EU", "AT": "EU", "PT": "EU", "IE": "EU", "GR": "EU",
        "PL": "EU", "SE": "EU", "FI": "EU", "DK": "EU", "CZ": "EU",
        # Others
        "US": "US", "GB": "UK", "UK": "UK", "IN": "IN", "SG": "SG",
        "JP": "JP", "BR": "BR", "CN": "CN", "RU": "RU", "AU": "AU",
    }
    
    # Countries with data localization requirements
    DATA_LOCALIZATION = {
        "IN": {"regulation": "RBI Data Localization", "strict": True, "sectors": ["payments"]},
        "RU": {"regulation": "Federal Law 242-FZ", "strict": True, "sectors": ["all"]},
        "CN": {"regulation": "PIPL/CSL", "strict": True, "sectors": ["all"]},
        "ID": {"regulation": "GR 71/2019", "strict": False, "sectors": ["government"]},
    }
    
    # EU Adequacy Decisions (countries with "essentially equivalent" protection)
    EU_ADEQUACY = ["UK", "JP", "KR", "AR", "NZ", "CH", "IL", "CA", "UY"]
    
    # Known regulatory conflicts
    KNOWN_CONFLICTS = [
        {
            "id": "CONFLICT-001",
            "type": "data_localization",
            "regulations": ["GDPR", "RBI Data Localization"],
            "description": "EU data subject's card used in India - conflicting storage requirements",
            "resolution": "Store copy in India for local transaction processing, primary in EU",
            "risk_level": "medium"
        },
        {
            "id": "CONFLICT-002",
            "type": "retention_duration",
            "regulations": ["GDPR Art 5(1)(e)", "Tax Law"],
            "description": "GDPR requires data minimization, tax laws require 7-year retention",
            "resolution": "Separate tax-required data from general personal data. Apply targeted retention.",
            "risk_level": "low"
        },
        {
            "id": "CONFLICT-003",
            "type": "cross_border_transfer",
            "regulations": ["GDPR Art 44", "CCPA"],
            "description": "EU-to-US data transfers post Schrems II require additional safeguards",
            "resolution": "Implement Standard Contractual Clauses (SCCs) and transfer impact assessments",
            "risk_level": "high"
        },
        {
            "id": "CONFLICT-004",
            "type": "consent_standard",
            "regulations": ["GDPR", "LGPD"],
            "description": "GDPR requires explicit consent, LGPD allows implied consent in some cases",
            "resolution": "Apply stricter GDPR standard when both jurisdictions apply",
            "risk_level": "low"
        }
    ]
    
    def __init__(self):
        """Initialize the cross-jurisdiction analyzer"""
        self.analysis_cache = {}
    
    def get_region(self, country_code: str) -> str:
        """Map country code to regulatory region"""
        return self.COUNTRY_TO_REGION.get(country_code.upper(), "OTHER")
    
    def get_applicable_regulations(self, countries: list[str]) -> dict:
        """Get all applicable regulations for a set of countries"""
        regulations = {}
        
        for country in countries:
            region = self.get_region(country)
            if region in self.JURISDICTION_REGS:
                regulations[region] = self.JURISDICTION_REGS[region]
        
        # Always add global regulations
        regulations["GLOBAL"] = self.JURISDICTION_REGS["GLOBAL"]
        
        return regulations
    
    def check_data_localization(self, countries: list[str]) -> list[dict]:
        """Check if any country has data localization requirements"""
        requirements = []
        
        for country in countries:
            if country.upper() in self.DATA_LOCALIZATION:
                loc = self.DATA_LOCALIZATION[country.upper()]
                requirements.append({
                    "country": country,
                    "regulation": loc["regulation"],
                    "strict": loc["strict"],
                    "sectors": loc["sectors"],
                    "requirement": f"Data must be stored locally in {country}"
                })
        
        return requirements
    
    def check_eu_adequacy(self, destination: str) -> dict:
        """Check if destination has EU adequacy decision"""
        is_adequate = destination.upper() in self.EU_ADEQUACY or destination.upper() in ["DE", "FR", "IT", "ES", "NL"]
        
        return {
            "destination": destination,
            "has_adequacy": is_adequate,
            "mechanism_required": "None" if is_adequate else "SCCs or BCRs required",
            "notes": "EU adequacy decision in place" if is_adequate else "Standard Contractual Clauses recommended"
        }
    
    def analyze_transaction(self, transaction: dict) -> dict:
        """
        Analyze a transaction's cross-jurisdiction compliance
        
        Input: {
            origin_country: str,
            processor_country: str,
            settlement_country: str,
            card_issuing_country: Optional[str],
            merchant_country: Optional[str],
            data_types: Optional[list[str]]
        }
        
        Output: Full compliance analysis
        """
        # Extract countries from transaction
        countries = set()
        countries.add(transaction.get("origin_country", "US"))
        countries.add(transaction.get("processor_country", "US"))
        countries.add(transaction.get("settlement_country", "US"))
        
        if transaction.get("card_issuing_country"):
            countries.add(transaction["card_issuing_country"])
        if transaction.get("merchant_country"):
            countries.add(transaction["merchant_country"])
        
        countries = list(countries)
        
        # Get applicable regulations
        regulations = self.get_applicable_regulations(countries)
        
        # Check for data localization requirements
        localization = self.check_data_localization(countries)
        
        # Check for conflicts
        conflicts = self.get_jurisdiction_conflicts(list(regulations.keys()))
        
        # Determine overall compliance status
        compliance_status = "COMPLIANT"
        conditions = []
        risks = []
        
        # Check EU data transfers
        eu_involved = "EU" in regulations
        if eu_involved:
            for country in countries:
                region = self.get_region(country)
                if region not in ["EU", "UK"]:
                    adequacy = self.check_eu_adequacy(country)
                    if not adequacy["has_adequacy"]:
                        conditions.append(f"SCCs required for EU → {country} data transfer")
                        risks.append(f"GDPR adequacy may change - monitor {country}")
        
        # Check localization requirements
        if localization:
            for loc in localization:
                conditions.append(loc["requirement"])
                if loc["strict"]:
                    risks.append(f"{loc['country']} has strict localization - data copies required")
        
        # Add conflict-based risks
        for conflict in conflicts:
            if conflict["risk_level"] in ["high", "medium"]:
                risks.append(conflict["description"])
        
        return {
            "transaction_id": transaction.get("id", f"TXN-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"),
            "analyzed_at": datetime.utcnow().isoformat() + "Z",
            "jurisdictions": countries,
            "regions": list(regulations.keys()),
            "applicable_regulations": regulations,
            "compliance_status": compliance_status,
            "data_localization_requirements": localization,
            "conflicts": conflicts,
            "conditions": conditions,
            "risks": risks,
            "guidance": self._generate_guidance(countries, regulations, conflicts)
        }
    
    def check_data_flow_compliance(self, origin: str, destination: str) -> dict:
        """
        Check if data can legally flow between two jurisdictions
        
        Returns: {allowed: bool, requirements: list, warnings: list}
        """
        origin_region = self.get_region(origin)
        dest_region = self.get_region(destination)
        
        requirements = []
        warnings = []
        allowed = True
        
        # EU origin checks
        if origin_region == "EU" and dest_region != "EU":
            adequacy = self.check_eu_adequacy(destination)
            if not adequacy["has_adequacy"]:
                requirements.append("Standard Contractual Clauses (SCCs) must be in place")
                requirements.append("Transfer Impact Assessment recommended")
                warnings.append("Post-Schrems II, additional safeguards may be needed for US transfers")
        
        # Data localization destination checks
        localization = self.check_data_localization([origin, destination])
        for loc in localization:
            if loc["strict"]:
                requirements.append(f"{loc['regulation']}: {loc['requirement']}")
                if loc["country"] == origin:
                    warnings.append(f"Data originating from {origin} may need local copy")
        
        # Check cross-border payment specific rules
        if origin == "IN" or destination == "IN":
            requirements.append("RBI: Payment data must be stored on servers in India")
        
        return {
            "origin": origin,
            "destination": destination,
            "origin_region": origin_region,
            "destination_region": dest_region,
            "allowed": allowed,
            "requirements": requirements,
            "warnings": warnings,
            "applicable_regulations": {
                "origin": self.JURISDICTION_REGS.get(origin_region, []),
                "destination": self.JURISDICTION_REGS.get(dest_region, []),
            }
        }
    
    def get_jurisdiction_conflicts(self, jurisdictions: list[str]) -> list[dict]:
        """
        Find conflicting requirements between jurisdictions
        
        Returns list of applicable conflicts
        """
        applicable_conflicts = []
        
        for conflict in self.KNOWN_CONFLICTS:
            # Check if conflict involves any of the jurisdictions
            for reg in conflict["regulations"]:
                for jur in jurisdictions:
                    if jur in self.JURISDICTION_REGS:
                        if any(reg.startswith(r) or r.startswith(reg.split()[0]) 
                               for r in self.JURISDICTION_REGS[jur]):
                            applicable_conflicts.append(conflict)
                            break
        
        # Remove duplicates
        seen = set()
        unique_conflicts = []
        for c in applicable_conflicts:
            if c["id"] not in seen:
                seen.add(c["id"])
                unique_conflicts.append(c)
        
        return unique_conflicts
    
    def _generate_guidance(self, countries: list[str], regulations: dict, conflicts: list[dict]) -> dict:
        """Generate human-readable compliance guidance"""
        
        # Build guidance
        key_requirements = []
        action_items = []
        
        # Add regulation-specific guidance
        if "EU" in regulations:
            key_requirements.append("GDPR Art 44-49: Ensure legal basis for cross-border transfers")
            key_requirements.append("Maintain Records of Processing Activities (ROPA)")
            action_items.append("Verify Data Processing Agreements with all processors")
        
        if "US" in regulations:
            key_requirements.append("CCPA: Provide opt-out rights for California residents")
            key_requirements.append("GLBA: Implement safeguards for financial information")
        
        if "IN" in regulations:
            key_requirements.append("RBI: Store payment data on servers in India")
            action_items.append("Confirm data residency compliance with Indian operations")
        
        if "SG" in regulations:
            key_requirements.append("PDPA: Appoint Data Protection Officer for Singapore operations")
        
        # Always add PCI-DSS
        key_requirements.append("PCI-DSS: Maintain cardholder data security standards")
        key_requirements.append("Retain transaction records per applicable retention periods")
        
        # Add conflict resolutions as action items
        for conflict in conflicts:
            action_items.append(f"Review: {conflict['resolution']}")
        
        return {
            "summary": f"Transaction involves {len(countries)} jurisdictions with {len(regulations)} regulatory frameworks",
            "key_requirements": key_requirements[:5],  # Limit to top 5
            "action_items": action_items[:5],  # Limit to top 5
            "documentation_needed": [
                "Data Processing Agreements",
                "Transfer Impact Assessment (if EU data)",
                "Consent records",
                "Evidence of encryption in transit and at rest"
            ]
        }
    
    def get_all_known_conflicts(self) -> list[dict]:
        """Return all known regulatory conflicts for reference"""
        return self.KNOWN_CONFLICTS
    
    def get_jurisdiction_summary(self, country: str) -> dict:
        """Get summary of a jurisdiction's regulatory landscape"""
        region = self.get_region(country)
        regs = self.JURISDICTION_REGS.get(region, [])
        
        has_localization = country.upper() in self.DATA_LOCALIZATION
        localization_info = self.DATA_LOCALIZATION.get(country.upper(), None)
        
        return {
            "country": country,
            "region": region,
            "regulations": regs,
            "has_data_localization": has_localization,
            "localization_details": localization_info,
            "eu_adequacy": country.upper() in self.EU_ADEQUACY
        }


# Demo function
def demo_analysis():
    """Demo the analyzer with sample data"""
    analyzer = CrossJurisdictionAnalyzer()
    
    # Sample cross-border transaction
    transaction = {
        "id": "TXN-DEMO-001",
        "origin_country": "DE",  # Germany (EU)
        "processor_country": "SG",  # Singapore
        "settlement_country": "US",  # United States
        "card_issuing_country": "DE",
        "merchant_country": "SG"
    }
    
    result = analyzer.analyze_transaction(transaction)
    print(f"Analysis Result: {result}")
    return result


if __name__ == "__main__":
    demo_analysis()
