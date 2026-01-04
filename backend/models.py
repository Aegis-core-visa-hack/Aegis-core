"""Pydantic models for AEGIS API"""
from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

# Enums as Literals
Severity = Literal["critical", "high", "medium", "low"]
RiskLevel = Literal["high", "medium", "low"]
AlertStatus = Literal["open", "investigating", "resolved", "false_positive"]
EntityType = Literal["bank", "merchant", "vendor"]
PCIStatus = Literal["valid", "expiring", "expired"]
AgentStatus = Literal["online", "offline", "running", "error"]


# Dashboard Models
class MetricChange(BaseModel):
    value: float | int
    change: float | int
    trend: Literal["up", "down", "stable"]


class AgentInfo(BaseModel):
    id: int
    name: str
    display_name: str
    status: AgentStatus
    last_run: str
    description: str
    stats: Optional[str] = None


class DashboardSummary(BaseModel):
    compliance_score: MetricChange
    at_risk_entities: MetricChange
    violations_24h: MetricChange
    agents_online: int
    agents_total: int


class RiskHeatmapItem(BaseModel):
    name: str
    risk_level: RiskLevel
    score: int
    open_violations: int
    jurisdiction: str


# Alert Models
class AlertBase(BaseModel):
    id: str
    severity: Severity
    title: str
    description: str
    timestamp: str
    entity_id: Optional[str]
    regulation: str
    status: AlertStatus


class AlertDetail(AlertBase):
    evidence: str
    recommendations: list[str]
    context: dict


# Entity Models
class Entity(BaseModel):
    id: str
    name: str
    type: EntityType
    pci_status: PCIStatus
    pci_expiry: str
    risk_level: RiskLevel
    violation_count: int


class EntityDetail(Entity):
    country: Optional[str] = None
    violations: list[AlertBase] = []


# Chat Models
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    suggested_actions: list[str]
    conversation_id: str


# API Response Wrappers
class APIResponse(BaseModel):
    data: dict | list
    message: Optional[str] = None


class PaginatedResponse(BaseModel):
    data: list
    pagination: dict
