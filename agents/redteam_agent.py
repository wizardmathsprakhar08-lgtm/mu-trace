import json
from typing import List, Dict, Any
from core.schema import RedTeamOutput, RedTeamIssue, SectionDraft, EvidenceItem
from agents.llm_router import LLMRouter

SYSTEM_PROMPT = """You are a cynical, forensic short-seller equity analyst.
Your job is to identify every blind spot, weak assumption, debt overhang, revenue concentration risk, and unproven management optimism in the draft report.
Look for:
1. One-sided bull cases lacking downcycle stress-testing.
2. Stretched working capital cycles or capital expenditure overruns.
3. Accounting divergence between reported EBITDA and operating cash flows.
4. Specific market triggers that could break the thesis ("What would make us wrong").
"""

class RedTeamAgent:
    """
    Stage 6: Adversarial Short-Seller Agent providing harsh counter-thesis and stress test.
    """
    @classmethod
    def critique_report(
        cls, 
        ticker: str, 
        company_name: str, 
        sections: List[SectionDraft], 
        evidence_text: str
    ) -> RedTeamOutput:
        
        draft_summary = []
        for s in sections:
            draft_summary.append(f"### {s.name}")
            for p in s.paragraphs:
                draft_summary.append(f"- [{p.claim_id}] {p.text}")
        draft_text = "\n".join(draft_summary)
        
        user_prompt = f"""Task: You are a skeptical short-seller analyst. Given the draft report for {company_name} ({ticker}) and the evidence, find:
(a) claims the evidence does not support or that ignore downside risk,
(b) balance sheet and cash flow risks the draft downplayed,
(c) weak or one-sided bullish reasoning,
(d) key thesis failure points ("what would make us wrong").

Draft:
{draft_text[:2500]}

Evidence:
{evidence_text[:1500]}

Return JSON strictly:
{{
  "issues": [
    {{
      "claim_id": "CLM-S1-P1",
      "problem": "...",
      "severity": "high|med|low",
      "evidence_ref": "S1",
      "suggested_fix": "..."
    }}
  ],
  "what_would_make_us_wrong": [
    "3 to 5 concrete conditions that invalidate the thesis"
  ],
  "bear_case_thesis": "A rigorous 2-sentence bear case synopsis."
}}
"""
        raw = LLMRouter.call_model(SYSTEM_PROMPT, user_prompt, temperature=0.4)
        data = LLMRouter.clean_json_output(raw)
        
        issues = []
        for i, itm in enumerate(data.get("issues", [])):
            issues.append(RedTeamIssue(
                issue_id=f"RT-{i+1:03d}",
                claim_id=itm.get("claim_id"),
                problem=itm.get("problem", "Unaddressed downside vulnerability"),
                severity=itm.get("severity", "med"),
                evidence_ref=itm.get("evidence_ref"),
                suggested_fix=itm.get("suggested_fix", "Incorporate downside sensitivity")
            ))
            
        wwmuw = data.get("what_would_make_us_wrong", [
            "Unexpected commodity or input cost spikes compressing EBITDA margins by >200 bps.",
            "Higher-for-longer interest rates increasing rollover costs on outstanding debt obligations.",
            "Execution delays on major capital expenditure pipelines muting return on capital employed."
        ])
        
        bear_thesis = data.get("bear_case_thesis", 
            "Downside risks stem from deteriorating working capital efficiency and potential demand softness in export end-markets, which could derate multiple expansion expectations."
        )
        
        return RedTeamOutput(
            issues=issues,
            what_would_make_us_wrong=wwmuw,
            bear_case_thesis=bear_thesis
        )
