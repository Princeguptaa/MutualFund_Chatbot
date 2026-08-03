# Dictionary mapping user queries/aliases to canonical scheme names
ALIAS_MAP = {
    # SBI Schemes
    "sbi bluechip fund": "SBI Large Cap Fund",
    "sbi large cap": "SBI Large Cap Fund",
    "sbi flexi cap fund": "SBI Flexicap Fund",
    "sbi flexicap": "SBI Flexicap Fund",
    "sbi small cap": "SBI Small Cap Fund",
    
    # Nippon India Schemes
    "nippon india small cap": "Nippon India Small Cap Fund",
    "nippon small cap": "Nippon India Small Cap Fund",
    
    # HDFC Schemes
    "hdfc flexi cap fund": "HDFC Flexi Cap Fund",
    "hdfc flexicap": "HDFC Flexi Cap Fund",
    "hdfc mid-cap opportunities": "HDFC Mid-Cap Opportunities Fund",
    "hdfc mid cap": "HDFC Mid-Cap Opportunities Fund",
    
    # ICICI Prudential Schemes
    "icici prudential bluechip fund": "ICICI Prudential Bluechip Fund",
    "icici bluechip": "ICICI Prudential Bluechip Fund",
    "icici prudential value discovery": "ICICI Prudential Value Discovery Fund",
    "icici value discovery": "ICICI Prudential Value Discovery Fund"
}

def get_canonical_schemes():
    return list(set(ALIAS_MAP.values()))
