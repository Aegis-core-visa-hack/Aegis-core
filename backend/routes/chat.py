"""Chat API routes with Gemini integration"""
import os
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/chat", tags=["Chat"])


class ChatMessage(BaseModel):
    message: str
    conversation_id: Optional[str] = None


# Mock response for when Gemini is not available
def get_mock_response(query: str) -> str:
    """Return a mock response for demo purposes"""
    query_lower = query.lower()
    
    if "expir" in query_lower or "certification" in query_lower:
        return """Based on my analysis, I found **3 member banks** with PCI certifications expiring within 30 days:

| Bank ID | Name | Expiry Date | Days Left | Risk |
|---------|------|-------------|-----------|------|
| BNK-1234 | First National Bank | 2026-01-15 | 10 | 🔴 High |
| BNK-5678 | Metro Credit Union | 2026-01-22 | 17 | 🟡 Medium |
| BNK-9012 | Pacific Trust | 2026-02-01 | 27 | 🟡 Medium |

**Recommended Actions:**
1. Send certification renewal reminders immediately
2. Schedule compliance review calls
3. Prepare remediation support if needed"""

    if "violation" in query_lower or "critical" in query_lower:
        return """Current violation status:

| Severity | Count | Trend |
|----------|-------|-------|
| 🔴 Critical | 3 | ↑ +2 this week |
| 🟠 High | 12 | → Stable |
| 🟡 Medium | 23 | ↓ -3 this week |
| 🟢 Low | 9 | → Stable |

**Top Priority Issues:**
1. **ALT-001**: Transaction anomaly at Merchant MID-4521 (potential card testing)
2. **ALT-002**: PAN exposed in settlement log (PCI-DSS 3.4 violation)
3. **ALT-003**: Bank certification expiring in 5 days

Would you like me to generate a detailed report or take action on any of these?"""

    if "gdpr" in query_lower:
        return """**GDPR Overview:**

The General Data Protection Regulation applies to all organizations processing EU resident data.

**Key Requirements:**
- **Article 17**: Right to erasure ("right to be forgotten")
- **Article 30**: Records of processing activities
- **Article 33**: 72-hour breach notification

**Current AEGIS Status:**
- Compliance Score: 85%
- Open Violations: 8
- Risk Level: 🟡 Medium

**Recent Update:** New amendment published on data retention - impact analysis pending."""

    if "pci" in query_lower:
        return """**PCI-DSS Compliance Summary:**

PCI-DSS is the global payment card security standard.

**Current Status:**
- Overall Score: 72% (🔴 High Risk)
- Open Violations: 12
- Affected Entities: 4 merchants, 2 banks

**Key Requirements Under Review:**
- Requirement 3.4: Render PAN unreadable
- Requirement 10.2: Audit log monitoring
- Requirement 12.8: Vendor management

**Immediate Actions Needed:**
1. Resolve ALT-002 (PAN in logs)
2. Review Merchant MID-4521 transaction patterns
3. Follow up on expiring certifications"""

    # Default response
    return f"""Based on your query "{query}", here's what I found:

**Summary:** I've analyzed the current compliance landscape.

| Metric | Value | Trend |
|--------|-------|-------|
| Total Violations | 47 | ↑ +8 this week |
| Critical Issues | 3 | Requires attention |
| At-Risk Entities | 12 | 5 banks, 7 merchants |

**Recommendations:**
1. Prioritize the 3 critical alerts in the queue
2. Follow up on expiring certifications
3. Schedule compliance review for high-risk entities

Would you like me to generate a detailed report or take any specific action?"""


@router.post("")
async def chat(message: ChatMessage):
    """Process chat message and return AI response"""
    conversation_id = message.conversation_id or str(uuid.uuid4())
    
    # Try Gemini first, fall back to mock
    try:
        gemini_key = os.getenv("GEMINI_API_KEY")
        
        if gemini_key:
            import google.generativeai as genai
            
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("gemini-2.0-flash")
            
            system_prompt = """You are AEGIS, an AI compliance assistant for financial services.
You help with PCI-DSS, GDPR, CCPA, and other regulatory compliance.
Provide concise, actionable answers. Use tables when helpful.
If asked about specific data, provide mock examples."""
            
            response = model.generate_content(
                f"{system_prompt}\n\nUser: {message.message}"
            )
            
            response_text = response.text
        else:
            # Use mock response
            response_text = get_mock_response(message.message)
            
    except Exception as e:
        # Fall back to mock on any error
        response_text = get_mock_response(message.message)
    
    return {
        "data": {
            "response": response_text,
            "suggested_actions": ["Generate Report", "Send Reminders", "View Details"],
            "conversation_id": conversation_id,
        }
    }
