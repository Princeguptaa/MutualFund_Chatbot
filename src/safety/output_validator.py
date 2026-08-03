from src.safety.pii_detector import detect_pii
from src.safety.refusal_templates import advisory_refusal
import re

def validate_output(response: str) -> str:
    """
    Validates the generated response for safety constraints.
    Truncates if too long, replaces if advisory or PII is found.
    """
    # 1. PII check
    if detect_pii(response):
        return "The generated response was blocked due to potential PII exposure."
        
    # 2. Advisory scan
    advisory_keywords = ["recommend", "suggest", "should invest"]
    if any(kw in response.lower() for kw in advisory_keywords):
        return advisory_refusal()
        
    # 3. Truncate to <= 3 sentences (basic implementation)
    sentences = re.split(r'(?<=[.!?]) +', response.strip())
    if len(sentences) > 3:
        response = " ".join(sentences[:3])
        if not response.endswith(('.', '!', '?')):
            response += "."
            
    return response
