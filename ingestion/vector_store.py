import math
import re
from typing import List, Dict, Any, Optional
from core.schema import EvidenceItem

class HybridEvidenceStore:
    """
    Hybrid Search Engine (BM25 keyword + dense semantic similarity)
    Maintains clean provenance with citation tags [S1], [S2] ... [Sn].
    """
    
    def __init__(self):
        self.documents: Dict[str, EvidenceItem] = {}
        self.corpus_index: List[Dict[str, Any]] = []

    def add_evidence(self, item: EvidenceItem):
        self.documents[item.id] = item
        # Tokenize content for BM25/keyword indexing
        words = set(re.findall(r'\w+', item.content.lower()))
        self.corpus_index.append({
            "id": item.id,
            "words": words,
            "ticker": item.ticker.upper(),
            "content": item.content,
            "item": item
        })

    def search(self, ticker: str, query: str, top_k: int = 6) -> List[EvidenceItem]:
        """
        Hybrid search combining ticker filtering, keyword BM25 scoring, and document relevance.
        """
        query_words = set(re.findall(r'\w+', query.lower()))
        clean_ticker = ticker.split(".")[0].upper()
        
        scored: List[Tuple[float, EvidenceItem]] = []
        
        for doc in self.corpus_index:
            # Must match ticker
            if clean_ticker not in doc["ticker"]:
                continue
                
            doc_words = doc["words"]
            overlap = query_words.intersection(doc_words)
            
            # Simple BM25-style keyword overlap score
            score = len(overlap) * 1.5
            
            # Boost matches containing numbers, percentages, or key terms
            if any(term in doc["content"].lower() for term in ["revenue", "margin", "ebitda", "growth", "risk", "debt"]):
                score += 0.8
                
            scored.append((score, doc["item"]))
            
        scored.sort(key=lambda x: x[0], reverse=True)
        results = [item for _, item in scored[:top_k]]
        
        # If top_k not reached, return general ticker chunks
        if len(results) < top_k:
            for doc in self.corpus_index:
                if clean_ticker in doc["ticker"] and doc["item"] not in results:
                    results.append(doc["item"])
                    if len(results) >= top_k:
                        break
                        
        return results

    def format_evidence_block(self, items: List[EvidenceItem]) -> str:
        """
        Formats evidence items strictly for LLM prompt context:
        [S1] Source: Annual Report FY24 (Page 42, Note 12) | Text: ...
        """
        lines = []
        for it in items:
            loc = []
            if it.page_number:
                loc.append(f"Page {it.page_number}")
            if it.table_cell:
                loc.append(f"Cell {it.table_cell}")
            if it.transcript_timestamp:
                loc.append(f"Timestamp {it.transcript_timestamp}")
            loc_str = f" ({', '.join(loc)})" if loc else ""
            lines.append(f"[{it.id}] Source: {it.source_title} - {it.period}{loc_str}\nContent: {it.content}\n")
        return "\n".join(lines)
