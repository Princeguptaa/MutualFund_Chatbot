from src.safety.output_validator import validate_output
from typing import List, Dict, Any

def format_response(raw_answer: str, source_chunks: List[Dict[str, Any]]) -> str:
    """
    Validates the generated answer and injects citation and footer.
    """
    validated_response = validate_output(raw_answer)
    
    # We only inject citation if it's not a blocked message or an empty result
    if ("blocked due to potential PII exposure" in validated_response or 
        "cannot provide investment advice" in validated_response or
        "I do not have enough information" in validated_response):
        return validated_response
        
    if not source_chunks:
        return validated_response
        
    # Get metadata from the top chunk (most relevant)
    top_chunk = source_chunks[0]
    metadata = top_chunk.get("metadata", {})
    
    citation_url = metadata.get("source_url", "Unknown Source")
    last_verified = metadata.get("last_verified_date", "Unknown Date")
    
    formatted_response = f"{validated_response}\n\n"
    formatted_response += f"📎 Source: {citation_url}\n"
    formatted_response += f"🕐 Last updated from sources: {last_verified}"
    
    return formatted_response
