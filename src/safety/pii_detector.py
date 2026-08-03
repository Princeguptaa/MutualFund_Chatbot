import re
from typing import Optional
from dataclasses import dataclass

@dataclass
class PiiResult:
    pii_type: str
    matched: bool

def detect_pii(text: str) -> Optional[PiiResult]:
    """
    Detects PII in the given text using regex patterns.
    Returns PiiResult if PII is found, else None.
    """
    if not text:
        return None
        
    patterns = {
        "PAN": r"[A-Z]{5}[0-9]{4}[A-Z]{1}",
        "Aadhaar": r"\b\d{4}\s?\d{4}\s?\d{4}\b",
        "Email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
        "Phone": r"\b(?:\+91|91)?[6789]\d{9}\b",
        "OTP": r"\b\d{4,6}\b" # basic 4-6 digit OTP
    }
    
    for pii_type, pattern in patterns.items():
        if re.search(pattern, text):
            return PiiResult(pii_type=pii_type, matched=True)
            
    # Add a loose check for account numbers (e.g. 9-18 digits)
    if re.search(r"\b\d{9,18}\b", text):
        return PiiResult(pii_type="Account Number", matched=True)
        
    return None
