from typing import List, Dict, Any

def build_prompt(query: str, retrieved_chunks: List[Dict[str, Any]], scheme_name: str = None) -> str:
    """
    Constructs the prompt containing the system constraints, context, and user query.
    """
    system_prompt = (
        "You are a Mutual Fund Assistant. You must follow these strict rules:\n"
        "1. Answer ONLY using the provided context.\n"
        "2. Keep your answer to 3 sentences or less.\n"
        "3. Do not provide any investment advice or opinions.\n"
        "4. Be factual, concise, and direct.\n"
        "If the context does not contain the answer, say 'I do not have enough information to answer that based on the provided documents.'\n"
    )
    
    context_text = ""
    for i, chunk in enumerate(retrieved_chunks):
        source = chunk.get('metadata', {}).get('source_url', 'Unknown')
        scheme_prefix = f"Scheme: {scheme_name}\n" if scheme_name else ""
        context_text += f"\n--- Context {i+1} (Source: {source}) ---\n{scheme_prefix}{chunk['text']}\n"
        
    prompt = f"{system_prompt}\n\nContext:{context_text}\n\nUser Query: {query}\n\nAnswer:"
    return prompt
