"""
Agent 3: Transaction Monitor
Demo implementation for hackathon - PAN detection and anomaly flagging
"""
import re
from typing import Optional
from datetime import datetime


class TransactionMonitor:
    """Demo transaction monitoring agent with PAN detection"""
    
    # Card number regex patterns
    PAN_PATTERNS = [
        # Visa: starts with 4, 13-16 digits
        r'\b4[0-9]{12}(?:[0-9]{3})?\b',
        
        # Mastercard: starts with 51-55 or 2221-2720
        r'\b(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}\b',
        
        # AMEX: starts with 34 or 37, 15 digits
        r'\b3[47][0-9]{13}\b',
        
        # Discover: starts with 6011, 65, 644-649
        r'\b(?:6011|65[0-9]{2}|64[4-9][0-9])[0-9]{12}\b',
        
        # Generic with separators (4 groups of 4)
        r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
    ]
    
    def __init__(self):
        self.compiled_patterns = [re.compile(p) for p in self.PAN_PATTERNS]
    
    @staticmethod
    def luhn_check(card_number: str) -> bool:
        """Validate card number using Luhn algorithm"""
        # Remove non-digit characters
        digits = re.sub(r'\D', '', card_number)
        
        if len(digits) < 13 or len(digits) > 19:
            return False
        
        # Luhn algorithm
        total = 0
        reverse_digits = digits[::-1]
        
        for i, digit in enumerate(reverse_digits):
            n = int(digit)
            if i % 2 == 1:  # Double every second digit
                n *= 2
                if n > 9:
                    n -= 9
            total += n
        
        return total % 10 == 0
    
    def detect_card_type(self, card_number: str) -> Optional[str]:
        """Identify card type from number"""
        digits = re.sub(r'\D', '', card_number)
        
        if len(digits) < 13:
            return None
        
        if digits[0] == '4':
            return "Visa"
        elif digits[:2] in ['51', '52', '53', '54', '55'] or (2221 <= int(digits[:4]) <= 2720):
            return "Mastercard"
        elif digits[:2] in ['34', '37']:
            return "American Express"
        elif digits[:4] == '6011' or digits[:2] == '65' or digits[:3] in ['644', '645', '646', '647', '648', '649']:
            return "Discover"
        
        return "Unknown"
    
    def mask_pan(self, card_number: str) -> str:
        """Mask card number for safe logging"""
        digits = re.sub(r'\D', '', card_number)
        if len(digits) < 8:
            return "****"
        return f"{digits[:4]}-XXXX-XXXX-{digits[-4:]}"
    
    def scan_text(self, text: str, source: str = "unknown") -> list:
        """Scan text for PAN data"""
        violations = []
        
        for pattern in self.compiled_patterns:
            matches = pattern.findall(text)
            
            for match in matches:
                # Validate with Luhn
                if self.luhn_check(match):
                    card_type = self.detect_card_type(match)
                    masked = self.mask_pan(match)
                    
                    violations.append({
                        "type": "pan_detected",
                        "severity": "critical",
                        "matched_pattern": masked,
                        "card_type": card_type,
                        "source": source,
                        "detected_at": datetime.utcnow().isoformat() + "Z",
                        "recommendation": "Immediately remove or encrypt this data",
                    })
        
        return violations
    
    def scan_transaction_log(self, log_content: str) -> dict:
        """Scan a transaction log file for PCI violations"""
        violations = self.scan_text(log_content, source="transaction_log")
        
        return {
            "scanned_at": datetime.utcnow().isoformat() + "Z",
            "violations_found": len(violations),
            "violations": violations,
            "status": "critical" if violations else "clean",
        }


# Demo function to show capability
def demo_scan():
    """Demo the scanner with test data"""
    monitor = TransactionMonitor()
    
    # Test data with a real card number pattern (test card)
    test_log = """
    2026-01-05 08:45:22 | SETTLEMENT | 4532-1234-5678-9012 | $150.00
    2026-01-05 08:46:15 | AUTH | ****-****-****-3456 | $75.00
    2026-01-05 08:47:33 | REFUND | 5425233430109903 | $25.00
    """
    
    result = monitor.scan_transaction_log(test_log)
    print(f"Scan Result: {result}")
    return result


if __name__ == "__main__":
    demo_scan()
