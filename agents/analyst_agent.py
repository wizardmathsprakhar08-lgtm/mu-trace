import json
from typing import Dict, Any, List
from core.schema import SectionDraft, ParagraphClaim, MetricItem, EvidenceItem
from agents.llm_router import LLMRouter

SYSTEM_PROMPT = """You are a senior equity research analyst assistant. You write for an analyst who will review your work before anyone relies on it.

RULES:
1. Use ONLY the evidence supplied in <evidence> and <financials>. Never use outside memory for any company fact or number.
2. Every factual sentence must end with a citation tag [S#] that maps to an evidence item. If you have no evidence, write "Not found in provided sources" instead of guessing.
3. Never compute or retype a number yourself. Use the placeholder {{metric_id}} from <financials>; code will fill the value.
4. Separate FACT (sourced), INFERENCE (your reasoning, labelled), and OPINION (scenario views, labelled). Never blur them.
5. Report uncertainty: state confidence (high/medium/low) and why.
6. Do not give personal investment advice, price targets as certainties, or buy/sell instructions. Present scenarios.
7. Currency and units: INR, ₹ Crore. Fiscal year ends 31st March.
8. Output valid JSON matching the schema given. No extra text.
"""

class AnalystAgent:
    """
    Stage 4: Drafts each section with strict evidence citation and metric placeholders.
    """
    @classmethod
    def draft_section(
        cls, 
        section_name: str, 
        company_name: str, 
        ticker: str, 
        evidence_text: str, 
        metrics_table_text: str,
        section_idx: int = 1
    ) -> SectionDraft:
        user_prompt = f"""Task: Write the section "{section_name}" for {company_name} ({ticker}).
Inputs:
<evidence>
{evidence_text}
</evidence>

<financials>
{metrics_table_text}
</financials>

Return JSON:
{{
  "paragraphs": [
    {{
      "text": "... [S1] ... {{{{metric_id}}}} ...",
      "type": "FACT|INFERENCE|OPINION",
      "sources": ["S1"],
      "confidence": "high|medium|low"
    }}
  ],
  "gaps": []
}}
Write 150-250 words. Lead with the key point. Be specific.
"""
        raw = LLMRouter.call_model(SYSTEM_PROMPT, user_prompt, temperature=0.2)
        data = LLMRouter.clean_json_output(raw)
        
        paragraphs = []
        p_list = data.get("paragraphs", [])
        for i, p in enumerate(p_list):
            cid = f"CLM-S{section_idx}-P{i+1}"
            paragraphs.append(ParagraphClaim(
                claim_id=cid,
                text=p.get("text", ""),
                type=p.get("type", "FACT"),
                sources=p.get("sources", []),
                confidence=p.get("confidence", "high")
            ))
            
        return SectionDraft(
            name=section_name,
            paragraphs=paragraphs,
            gaps=data.get("gaps", [])
        )
