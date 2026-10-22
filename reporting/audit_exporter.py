import json
from pathlib import Path
from typing import Dict, Any
from core.schema import FullReport

class AuditExporter:
    """
    Exports clean machine-readable JSON representation of every claim,
    its citation source [S#], table cell/page, and verification verdict.
    """
    @classmethod
    def export_json(cls, report: FullReport, output_path: str) -> str:
        data = {
            "report_id": report.report_id,
            "ticker": report.ticker,
            "company_name": report.company_name,
            "currency": report.currency,
            "unit": report.unit,
            "generated_at": report.generated_at,
            "status": report.status,
            "audit_summary": report.audit_summary.model_dump(),
            "claims": [
                {
                    "claim_id": p.claim_id,
                    "section": sec.name,
                    "text": p.text,
                    "type": p.type,
                    "sources": p.sources,
                    "verdict": p.verdict,
                    "evidence_span": p.evidence_span,
                    "confidence": p.confidence,
                    "source_details": [
                        report.evidence_store[s_id].model_dump()
                        for s_id in p.sources if s_id in report.evidence_store
                    ]
                }
                for sec in report.sections
                for p in sec.paragraphs
            ],
            "metrics": {
                k: m.model_dump() for k, m in report.key_metrics.items()
            },
            "red_team_audit": report.red_team_critique.model_dump(),
            "change_detections": [c.model_dump() for c in report.change_detections],
            "compliance_disclaimer": report.compliance_disclaimer
        }
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        return output_path
