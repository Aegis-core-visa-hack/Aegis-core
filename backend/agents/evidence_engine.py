"""
AEGIS Agent 5: Evidence & Reporting Engine
==========================================
Generates audit-ready reports, evidence packages, and manages remediation workflow.
"""
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import hashlib
import json


class EvidenceEngine:
    """
    Agent 5 - Evidence & Reporting Engine
    
    Responsibilities:
    1. Generate compliance reports (quarterly, annual, on-demand)
    2. Compile evidence packages for audits
    3. Create and track remediation cases (GRC)
    4. Export data in regulatory-required formats
    """
    
    def __init__(self):
        self.report_counter = 1
        self.evidence_counter = 1
        self.case_counter = 1
        self.delivery_counter = 1
        
        # Mock storage for generated reports and cases
        self.reports: Dict[str, Dict] = {}
        self.evidence_packages: Dict[str, Dict] = {}
        self.grc_cases: Dict[str, Dict] = {}
        
        # Report templates
        self.report_templates = {
            "PCI-DSS": {
                "title": "PCI-DSS Compliance Report",
                "sections": ["executive_summary", "requirements_mapping", "controls", "exceptions", "remediation"],
                "requirements_count": 250
            },
            "GDPR": {
                "title": "GDPR Compliance Report",
                "sections": ["executive_summary", "processing_records", "subject_requests", "cross_border", "breaches"],
                "requirements_count": 99
            },
            "SOC2": {
                "title": "SOC2 Type II Report",
                "sections": ["executive_summary", "control_objectives", "test_results", "exceptions"],
                "requirements_count": 64
            },
            "RBI": {
                "title": "RBI Compliance Report",
                "sections": ["executive_summary", "data_localization", "reporting_requirements", "exceptions"],
                "requirements_count": 45
            }
        }
        
        # SLA definitions by priority
        self.sla_hours = {
            "critical": 4,
            "high": 24,
            "medium": 72,
            "low": 168  # 7 days
        }
    
    def compile_evidence_package(
        self,
        scope: str = "full",
        timeframe_start: Optional[str] = None,
        timeframe_end: Optional[str] = None,
        entity_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Compile an audit-ready evidence package.
        
        Args:
            scope: "full", "pci", "gdpr", or "entity"
            timeframe_start: Start date (ISO format)
            timeframe_end: End date (ISO format)
            entity_id: Specific entity ID if scope is "entity"
        
        Returns:
            Evidence package metadata with download URL
        """
        from mock_data import alerts, entities, dashboard_summary
        
        # Default timeframe: last 90 days
        if not timeframe_end:
            timeframe_end = datetime.now().isoformat()
        if not timeframe_start:
            timeframe_start = (datetime.now() - timedelta(days=90)).isoformat()
        
        package_id = f"EVD-2026-{self.evidence_counter:03d}"
        self.evidence_counter += 1
        
        # Gather data based on scope
        if scope == "pci":
            filtered_alerts = [a for a in alerts if "PCI" in a.get("regulation", "")]
            filtered_entities = entities
            scope_label = "PCI-DSS"
        elif scope == "gdpr":
            filtered_alerts = [a for a in alerts if "GDPR" in a.get("regulation", "")]
            filtered_entities = [e for e in entities if e.get("country") in ["EU", "UK", "DE", "FR"]]
            scope_label = "GDPR"
        elif scope == "entity" and entity_id:
            filtered_alerts = [a for a in alerts if a.get("entity_id") == entity_id]
            filtered_entities = [e for e in entities if e["id"] == entity_id]
            scope_label = f"Entity {entity_id}"
        else:
            filtered_alerts = alerts
            filtered_entities = entities
            scope_label = "Full Audit"
        
        # Calculate summary metrics
        total_violations = len(filtered_alerts)
        critical_violations = len([a for a in filtered_alerts if a.get("severity") == "critical"])
        resolved = len([a for a in filtered_alerts if a.get("status") == "resolved"])
        
        # Generate checksum for integrity
        content_hash = hashlib.sha256(
            json.dumps({
                "alerts": filtered_alerts,
                "entities": [e["id"] for e in filtered_entities],
                "timeframe": f"{timeframe_start} to {timeframe_end}"
            }).encode()
        ).hexdigest()[:16]
        
        # Create package metadata
        package = {
            "package_id": package_id,
            "created_at": datetime.now().isoformat(),
            "scope": scope,
            "scope_label": scope_label,
            "timeframe": f"{timeframe_start[:10]} to {timeframe_end[:10]}",
            "contents": [
                "executive_summary.pdf",
                "violation_details.pdf",
                "entity_compliance_status.pdf",
                "audit_trail.csv",
                "raw_data.json"
            ],
            "summary": {
                "total_violations": total_violations,
                "critical": critical_violations,
                "resolved": resolved,
                "entities_covered": len(filtered_entities),
                "compliance_score": dashboard_summary["compliance_score"]["value"]
            },
            "download_url": f"/api/reports/{package_id}/download",
            "size_bytes": 2456789 + (total_violations * 1000),
            "checksum": f"sha256:{content_hash}...",
            "status": "ready"
        }
        
        # Store for later retrieval
        self.evidence_packages[package_id] = package
        
        return package
    
    def generate_regulatory_report(
        self,
        framework: str,
        region: Optional[str] = None,
        timeframe_start: Optional[str] = None,
        timeframe_end: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a report for a specific regulatory framework.
        
        Args:
            framework: "PCI-DSS", "GDPR", "SOC2", "RBI"
            region: Geographic scope (e.g., "US", "EU", "IN")
            timeframe_start: Start of reporting period
            timeframe_end: End of reporting period
        
        Returns:
            Report metadata with summary and download URL
        """
        from mock_data import alerts, dashboard_summary
        
        if framework not in self.report_templates:
            return {"error": f"Unknown framework: {framework}. Supported: {list(self.report_templates.keys())}"}
        
        template = self.report_templates[framework]
        
        # Default to current quarter
        if not timeframe_end:
            timeframe_end = datetime.now().isoformat()
        if not timeframe_start:
            timeframe_start = (datetime.now() - timedelta(days=90)).isoformat()
        
        # Generate report ID
        quarter = f"Q{((datetime.now().month - 1) // 3) + 1}"
        report_id = f"RPT-2026-{quarter}-{framework.replace('-', '')}"
        
        # Filter alerts by framework
        framework_alerts = [a for a in alerts if framework in a.get("regulation", "")]
        
        # Calculate compliance metrics
        total_violations = len(framework_alerts)
        critical_count = len([a for a in framework_alerts if a.get("severity") == "critical"])
        resolved_count = len([a for a in framework_alerts if a.get("status") == "resolved"])
        
        # Calculate requirement compliance (mock)
        total_requirements = template["requirements_count"]
        compliant = int(total_requirements * 0.92)
        exceptions = int(total_requirements * 0.05)
        not_applicable = total_requirements - compliant - exceptions
        
        compliance_score = round((compliant / total_requirements) * 100, 1)
        
        # Generate executive summary (simulated LLM output)
        executive_summary = self._generate_executive_summary(
            framework=framework,
            timeframe=f"{timeframe_start[:10]} to {timeframe_end[:10]}",
            violations=total_violations,
            critical=critical_count,
            resolved=resolved_count,
            score=compliance_score
        )
        
        report = {
            "report_id": report_id,
            "title": f"{template['title']} {quarter} 2025",
            "framework": framework,
            "region": region or "Global",
            "generated_at": datetime.now().isoformat(),
            "timeframe": f"{timeframe_start[:10]} to {timeframe_end[:10]}",
            "summary": {
                "compliance_score": compliance_score,
                "total_requirements": total_requirements,
                "compliant": compliant,
                "exceptions": exceptions,
                "not_applicable": not_applicable
            },
            "violations": {
                "total": total_violations,
                "critical": critical_count,
                "resolved": resolved_count,
                "open": total_violations - resolved_count
            },
            "executive_summary": executive_summary,
            "sections": template["sections"],
            "download_url": f"/api/reports/{report_id}/download",
            "pages": 24 + (total_violations * 2),
            "status": "ready"
        }
        
        # Store for later retrieval
        self.reports[report_id] = report
        
        return report
    
    def _generate_executive_summary(
        self,
        framework: str,
        timeframe: str,
        violations: int,
        critical: int,
        resolved: int,
        score: float
    ) -> str:
        """Generate an executive summary paragraph (simulated LLM output)."""
        return f"""During the reporting period ({timeframe}), the organization maintained a {score}% compliance score against {framework} requirements. A total of {violations} violations were identified, of which {critical} were classified as critical severity. The remediation team successfully resolved {resolved} issues, demonstrating proactive risk management.

Key areas requiring attention include enhanced monitoring of data handling procedures and continued investment in security controls. The compliance posture has improved compared to the previous quarter, with notable progress in automated detection capabilities.

Management should prioritize the remaining open findings, particularly those classified as critical, to maintain regulatory standing and reduce potential exposure to penalties."""
    
    def create_grc_case(
        self,
        title: str,
        description: str,
        priority: str = "medium",
        assigned_to: Optional[str] = None,
        linked_violation_id: Optional[str] = None,
        linked_entity_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a GRC (Governance, Risk, Compliance) case for tracking.
        
        Args:
            title: Case title
            description: Detailed description of the issue
            priority: "critical", "high", "medium", "low"
            assigned_to: Email of assignee (optional, auto-assigned if not specified)
            linked_violation_id: Optional alert/violation ID
            linked_entity_id: Optional entity ID
        
        Returns:
            Created case with SLA and action items
        """
        case_id = f"GRC-2026-{self.case_counter:05d}"
        self.case_counter += 1
        
        # Normalize priority
        priority = priority.lower()
        if priority not in self.sla_hours:
            priority = "medium"
        
        # Calculate SLA due date
        sla = self.sla_hours[priority]
        due_date = datetime.now() + timedelta(hours=sla)
        
        # Auto-assign if not specified
        if not assigned_to:
            # Mock round-robin assignment
            analysts = ["sarah.compliance@visa.com", "james.analyst@visa.com", "maria.auditor@visa.com"]
            assigned_to = analysts[self.case_counter % len(analysts)]
        
        case = {
            "case_id": case_id,
            "title": title,
            "description": description,
            "status": "open",
            "priority": priority,
            "assigned_to": assigned_to,
            "created_at": datetime.now().isoformat(),
            "due_date": due_date.isoformat(),
            "sla_hours": sla,
            "linked_violation_id": linked_violation_id,
            "linked_entity_id": linked_entity_id,
            "action_items": [
                {"step": 1, "action": "Investigate issue", "status": "pending"},
                {"step": 2, "action": "Determine root cause", "status": "pending"},
                {"step": 3, "action": "Implement fix", "status": "pending"},
                {"step": 4, "action": "Verify resolution", "status": "pending"}
            ],
            "history": [
                {
                    "timestamp": datetime.now().isoformat(),
                    "action": "created",
                    "actor": "system",
                    "notes": f"Case created with {priority} priority"
                }
            ],
            "notifications_sent": {
                "email": True,
                "dashboard": True
            }
        }
        
        # Store case
        self.grc_cases[case_id] = case
        
        return case
    
    def update_remediation_status(
        self,
        case_id: str,
        status: str,
        notes: Optional[str] = None,
        evidence: Optional[str] = None,
        actor: str = "analyst@visa.com"
    ) -> Dict[str, Any]:
        """
        Update the status of a remediation case.
        
        Args:
            case_id: GRC case ID
            status: "investigating", "in_progress", "pending_review", "completed", "reopened"
            notes: Optional progress notes
            evidence: Optional evidence of resolution
            actor: Who made the update
        
        Returns:
            Updated case status
        """
        if case_id not in self.grc_cases:
            return {"error": f"Case {case_id} not found"}
        
        case = self.grc_cases[case_id]
        previous_status = case["status"]
        
        # Validate state transitions
        valid_transitions = {
            "open": ["investigating"],
            "investigating": ["in_progress", "open"],
            "in_progress": ["pending_review", "investigating"],
            "pending_review": ["completed", "in_progress"],
            "completed": ["reopened"],
            "reopened": ["investigating"]
        }
        
        if status not in valid_transitions.get(previous_status, []):
            return {
                "error": f"Invalid transition from '{previous_status}' to '{status}'",
                "valid_transitions": valid_transitions.get(previous_status, [])
            }
        
        # Update case
        case["status"] = status
        case["updated_at"] = datetime.now().isoformat()
        
        # Add to history
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": f"status_change",
            "previous_status": previous_status,
            "new_status": status,
            "actor": actor
        }
        if notes:
            history_entry["notes"] = notes
        if evidence:
            history_entry["evidence"] = evidence
        case["history"].append(history_entry)
        
        # If completed, calculate resolution time
        resolution_time = None
        sla_met = None
        if status == "completed":
            created = datetime.fromisoformat(case["created_at"])
            completed = datetime.now()
            resolution_time = str(completed - created)
            sla_met = (completed - created).total_seconds() / 3600 <= case["sla_hours"]
            case["resolution_time"] = resolution_time
            case["sla_met"] = sla_met
        
        return {
            "case_id": case_id,
            "previous_status": previous_status,
            "new_status": status,
            "updated_at": case["updated_at"],
            "notes_added": notes is not None,
            "evidence_added": evidence is not None,
            "resolution_time": resolution_time,
            "sla_met": sla_met
        }
    
    def get_grc_case(self, case_id: str) -> Optional[Dict[str, Any]]:
        """Get a GRC case by ID."""
        return self.grc_cases.get(case_id)
    
    def list_grc_cases(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        assigned_to: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List GRC cases with optional filters."""
        cases = list(self.grc_cases.values())
        
        if status:
            cases = [c for c in cases if c["status"] == status]
        if priority:
            cases = [c for c in cases if c["priority"] == priority]
        if assigned_to:
            cases = [c for c in cases if c["assigned_to"] == assigned_to]
        
        return sorted(cases, key=lambda x: x["created_at"], reverse=True)
    
    def get_report(self, report_id: str) -> Optional[Dict[str, Any]]:
        """Get a report or evidence package by ID."""
        return self.reports.get(report_id) or self.evidence_packages.get(report_id)
    
    def list_reports(
        self,
        framework: Optional[str] = None,
        report_type: str = "all"
    ) -> List[Dict[str, Any]]:
        """
        List generated reports.
        
        Args:
            framework: Filter by framework (e.g., "PCI-DSS")
            report_type: "reports", "evidence", or "all"
        
        Returns:
            List of report metadata
        """
        all_items = []
        
        if report_type in ["reports", "all"]:
            reports = list(self.reports.values())
            if framework:
                reports = [r for r in reports if r.get("framework") == framework]
            all_items.extend(reports)
        
        if report_type in ["evidence", "all"]:
            packages = list(self.evidence_packages.values())
            if framework:
                packages = [p for p in packages if framework.lower() in p.get("scope", "")]
            all_items.extend(packages)
        
        return sorted(all_items, key=lambda x: x.get("created_at", ""), reverse=True)
    
    def get_remediation_summary(self) -> Dict[str, Any]:
        """Get a summary of all remediation cases."""
        cases = list(self.grc_cases.values())
        
        if not cases:
            return {
                "total_cases": 0,
                "by_status": {},
                "by_priority": {},
                "overdue": 0,
                "avg_resolution_hours": None
            }
        
        now = datetime.now()
        overdue = 0
        resolution_times = []
        
        for case in cases:
            # Check if overdue
            if case["status"] not in ["completed", "reopened"]:
                due = datetime.fromisoformat(case["due_date"])
                if now > due:
                    overdue += 1
            
            # Collect resolution times
            if "resolution_time" in case:
                # Parse resolution time (simplified)
                resolution_times.append(case["sla_hours"])  # Approximate
        
        by_status = {}
        by_priority = {}
        for case in cases:
            status = case["status"]
            priority = case["priority"]
            by_status[status] = by_status.get(status, 0) + 1
            by_priority[priority] = by_priority.get(priority, 0) + 1
        
        return {
            "total_cases": len(cases),
            "by_status": by_status,
            "by_priority": by_priority,
            "overdue": overdue,
            "avg_resolution_hours": sum(resolution_times) / len(resolution_times) if resolution_times else None
        }
    
    def export_data(
        self,
        data_type: str,
        format: str = "json",
        filters: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Export data in various formats.
        
        Args:
            data_type: "violations", "cases", "entities", "reports"
            format: "json", "csv"
            filters: Optional filters
        
        Returns:
            Export metadata with data or download URL
        """
        from mock_data import alerts, entities
        
        if data_type == "violations":
            data = alerts
        elif data_type == "cases":
            data = list(self.grc_cases.values())
        elif data_type == "entities":
            data = entities
        elif data_type == "reports":
            data = list(self.reports.values()) + list(self.evidence_packages.values())
        else:
            return {"error": f"Unknown data type: {data_type}"}
        
        export_id = f"EXP-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        return {
            "export_id": export_id,
            "data_type": data_type,
            "format": format,
            "record_count": len(data),
            "created_at": datetime.now().isoformat(),
            "download_url": f"/api/reports/export/{export_id}.{format}",
            "data": data if format == "json" else None
        }


# Singleton instance
evidence_engine = EvidenceEngine()
