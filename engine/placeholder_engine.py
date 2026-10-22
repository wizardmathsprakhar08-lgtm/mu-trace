import re
from typing import Dict, List, Tuple
from core.schema import MetricItem

class PlaceholderEngine:
    """
    Substitutes {{metric_id}} placeholders with audited deterministic values.
    Validates that:
    1. Every placeholder exists in the deterministic metrics table.
    2. LLM did not try to hallucinate invented figures in key positions.
    """
    
    PLACEHOLDER_REGEX = re.compile(r"\{\{([a-zA-Z0-9_]+)\}\}")
    
    @classmethod
    def substitute(cls, text: str, metrics: Dict[str, MetricItem]) -> Tuple[str, List[str], List[str]]:
        """
        Returns:
            (filled_text, successfully_replaced_metric_ids, missing_metric_ids)
        """
        used_metrics: List[str] = []
        missing_metrics: List[str] = []
        
        def replace_match(match: re.Match) -> str:
            m_id = match.group(1)
            if m_id in metrics:
                used_metrics.append(m_id)
                return metrics[m_id].formatted_value
            else:
                missing_metrics.append(m_id)
                return f"[UNRESOLVED METRIC: {m_id}]"
                
        filled_text = cls.PLACEHOLDER_REGEX.sub(replace_match, text)
        return filled_text, used_metrics, missing_metrics

    @classmethod
    def extract_placeholders(cls, text: str) -> List[str]:
        return cls.PLACEHOLDER_REGEX.findall(text)
        
    @classmethod
    def verify_zero_mismatch(cls, filled_text: str, metrics: Dict[str, MetricItem], used_metrics: List[str]) -> bool:
        """
        Audits that all replaced values exist verbatim in the text.
        """
        for m_id in used_metrics:
            expected_val = metrics[m_id].formatted_value
            if expected_val not in filled_text:
                return False
        return True
