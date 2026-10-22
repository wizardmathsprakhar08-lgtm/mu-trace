import json
from typing import Dict, Any, List
from core.schema import PlanOutput, SectionPlan
from agents.llm_router import LLMRouter

SYSTEM_PROMPT = """You are a senior equity research analyst assistant. You write for an analyst who will review your work before anyone relies on it.

RULES:
1. Use ONLY the evidence supplied in <evidence> and <financials>. Never use outside memory for any company fact or number.
2. Every factual sentence must end with a citation tag [S#] that maps to an evidence item.
3. Never compute or retype a number yourself. Use the placeholder {{metric_id}} from <financials>; code will fill the value.
4. Separate FACT (sourced), INFERENCE (your reasoning, labelled), and OPINION (scenario views, labelled). Never blur them.
5. Report uncertainty: state confidence (high/medium/low) and why.
6. Do not give personal investment advice, price targets as certainties, or buy/sell instructions. Present scenarios.
7. Currency and units: INR, ₹ Crore. Fiscal year ends 31st March.
8. Output valid JSON matching the schema given. No extra text.
"""

class PlannerAgent:
    """
    Stage 1: Formulates structured research plan, questions to answer, data required, and flags gaps.
    """
    @classmethod
    def plan_report(cls, ticker: str, company_name: str, focus: str = "comprehensive") -> PlanOutput:
        user_prompt = f"""Task: Plan a research report on {company_name} ({ticker}) with focus {focus}.
Using <available_data_index>:
- Income Statement, Balance Sheet, Cash Flow (FY21 - FY24)
- Recent Quarterly Earnings Releases & Investor Transcripts
- Segment Revenue and Operating Margins
- Shareholding Pattern & Capital Structure

Return JSON strictly matching:
{{"sections":[{{"name":"...", "questions":["..."], "required_data":["..."], "missing_data":["..."]}}]}}
List every question the report must answer and which data answers it. Flag missing data instead of assuming it.
"""
        raw = LLMRouter.call_model(SYSTEM_PROMPT, user_prompt, temperature=0.1)
        data = LLMRouter.clean_json_output(raw)
        
        sections = []
        for s in data.get("sections", []):
            sections.append(SectionPlan(
                name=s.get("name", "Section"),
                questions=s.get("questions", []),
                required_data=s.get("required_data", []),
                missing_data=s.get("missing_data", [])
            ))
            
        return PlanOutput(
            ticker=ticker,
            company_name=company_name,
            focus=focus,
            sections=sections
        )
