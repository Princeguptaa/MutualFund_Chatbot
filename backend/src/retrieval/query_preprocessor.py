from typing import Tuple, Optional
from src.data.alias_map import ALIAS_MAP

def preprocess_query(query: str) -> Tuple[str, Optional[str], Optional[str]]:
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
            
    # Edge-case: Ambiguity
    if not detected_scheme:
        if any(term in query_lower for term in ["sip", "nav", "exit load", "expense ratio", "fund manager"]):
            return query, None, "Could you please specify which mutual fund you want this information for?"
        
    return query, detected_scheme, None
