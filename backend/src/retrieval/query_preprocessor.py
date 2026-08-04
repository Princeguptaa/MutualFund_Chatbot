from typing import Tuple, Optional
from src.data.alias_map import ALIAS_MAP

def preprocess_query(query: str, current_scheme: Optional[str] = None) -> Tuple[str, Optional[str], Optional[str]]:
    """
    Preprocesses the query.
    Returns (normalized_query, detected_scheme_name, clarification_needed).
    """
    query_lower = query.lower().strip()
    
    # Wait until after alias map check to see if we detected a scheme
    detected_scheme = None
    for alias, canonical in ALIAS_MAP.items():
        if alias in query_lower:
            detected_scheme = canonical
            break
            
    # Fallback to the context's current scheme if not explicitly mentioned
    if not detected_scheme and current_scheme:
        detected_scheme = current_scheme
            
    # Edge-case: Ambiguity
    if not detected_scheme:
        ambiguous_terms = ["nav of", "nav", "expense ratio of", "exit load for", "exit load", "fund manager of", "return of", "return", "aum", "riskometer", "risk"]
        if any(term in query_lower for term in ambiguous_terms) or "this" in query_lower:
            return query, None, "Could you please specify which mutual fund you want this information for?"
        
    return query, detected_scheme, None
