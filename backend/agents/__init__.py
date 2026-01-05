"""AEGIS Agent Package - AI-powered compliance monitoring agents"""
from .transaction_monitor import TransactionMonitor
from .ecosystem_tracker import EcosystemTracker

# Import other agents if they exist (may be added by other agent threads)
try:
    from .regulatory_monitor import RegulatoryMonitor
except ImportError:
    RegulatoryMonitor = None

try:
    from .cross_jurisdiction import CrossJurisdictionAnalyzer
except ImportError:
    CrossJurisdictionAnalyzer = None

try:
    from .evidence_engine import EvidenceEngine
except ImportError:
    EvidenceEngine = None

__all__ = ["TransactionMonitor", "EcosystemTracker"]

# Add to __all__ if they exist
if RegulatoryMonitor:
    __all__.append("RegulatoryMonitor")
if CrossJurisdictionAnalyzer:
    __all__.append("CrossJurisdictionAnalyzer")
if EvidenceEngine:
    __all__.append("EvidenceEngine")
