from typing import List, Dict, Optional, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime

class EvidenceItem(BaseModel):
    id: str = Field(..., description="Unique evidence ID like S1, S2")
    ticker: str
    company_name: str
    source_title: str
    doc_type: str = Field(..., description="Annual Report, Q3 Earnings, Transcript, Exchange Filing")
    period: str = Field(..., description="e.g. FY24, Q2FY25")
    page_number: Optional[int] = None
    table_cell: Optional[str] = None
    transcript_timestamp: Optional[str] = None
    content: str
    as_of_date: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))

class MetricItem(BaseModel):
    metric_id: str = Field(..., description="Deterministic key e.g. rev_growth_yoy, ttm_pe, ebitda_margin")
    display_name: str
    value: float
    formatted_value: str
    unit: str
    period: str
    formula: str = Field(..., description="Exact deterministic formula used")
    source_ref: str = Field(..., description="Filing line item / DB origin")

class ParagraphClaim(BaseModel):
    claim_id: str
    text: str
    type: Literal["FACT", "INFERENCE", "OPINION"]
    sources: List[str] = Field(default_factory=list, description="IDs of evidence like ['S1', 'S3']")
    confidence: Literal["high", "medium", "low"] = "high"
    verdict: Optional[Literal["SUPPORTED", "PARTIAL", "UNSUPPORTED"]] = None
    evidence_span: Optional[str] = None
    unsupported_reason: Optional[str] = None

class SectionDraft(BaseModel):
    name: str
    paragraphs: List[ParagraphClaim] = Field(default_factory=list)
    raw_markdown: Optional[str] = None
    gaps: List[str] = Field(default_factory=list)

class SectionPlan(BaseModel):
    name: str
    questions: List[str]
    required_data: List[str]
    missing_data: List[str] = Field(default_factory=list)

class PlanOutput(BaseModel):
    ticker: str
    company_name: str
    focus: str
    sections: List[SectionPlan]

class RedTeamIssue(BaseModel):
    issue_id: str
    claim_id: Optional[str] = None
    problem: str
    severity: Literal["high", "med", "low"]
    evidence_ref: Optional[str] = None
    suggested_fix: str

class RedTeamOutput(BaseModel):
    issues: List[RedTeamIssue] = Field(default_factory=list)
    what_would_make_us_wrong: List[str] = Field(default_factory=list)
    bear_case_thesis: str = ""

class ChangeDetectionItem(BaseModel):
    topic: str
    prior_quarter: str
    current_quarter: str
    delta_type: Literal["NEW_RISK", "GUIDANCE_REVISED", "MARGIN_HEADWIND", "GROWTH_ACCELERATION", "NEUTRAL"]
    tone_shift: str
    significance: Literal["HIGH", "MEDIUM", "LOW"]

class AuditVerificationSummary(BaseModel):
    total_claims: int
    supported_claims: int
    partial_claims: int
    unsupported_claims: int
    faithfulness_score: float
    numeric_accuracy: float
    citation_precision: float
    passed_audit: bool

class FullReport(BaseModel):
    report_id: str
    ticker: str
    company_name: str
    currency: str = "INR"
    unit: str = "₹ Crore"
    fy_end: str = "31st March"
    generated_at: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    as_of_date: str = Field(default_factory=lambda: datetime.now().strftime("%d %B %Y"))
    status: Literal["DRAFT", "VERIFIED", "APPROVED", "REJECTED"] = "VERIFIED"
    executive_summary: str
    key_metrics: Dict[str, MetricItem] = Field(default_factory=dict)
    sections: List[SectionDraft] = Field(default_factory=list)
    change_detections: List[ChangeDetectionItem] = Field(default_factory=list)
    red_team_critique: RedTeamOutput
    evidence_store: Dict[str, EvidenceItem] = Field(default_factory=dict)
    audit_summary: AuditVerificationSummary
    compliance_disclaimer: str
