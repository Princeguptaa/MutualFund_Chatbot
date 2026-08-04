from typing import List, Dict
from src.generation.generator import _get_client

def rewrite_query(query: str, history: List[Dict[str, str]]) -> str:
    """
    Rewrites the query using chat history to resolve pronouns and contextual references.
    """
    if not history:
        return query

    client = _get_client()
    
    # Format history for the prompt
    history_text = ""
    for msg in history[-4:]: # Only take the last 4 messages to avoid context overflow and keep focus on recent turns
        role = msg.get("role", "unknown")
        text = msg.get("text", "")
        if role in ["user", "assistant"]:
            history_text += f"{role.capitalize()}: {text}\n"

    system_prompt = (
        "You are an assistant that rewrites follow-up questions to be standalone queries.\n"
        "Given the following chat history and a new user query, rewrite the query to be standalone, "
        "replacing any pronouns or contextual references (like 'it', 'this fund', 'that scheme') "
        "with the specific mutual fund or topic being discussed.\n"
        "If the query is already standalone or no specific context applies, return it exactly as is.\n"
        "IMPORTANT: Respond with ONLY the rewritten query text. Do not include any explanations, quotes, or conversational filler."
    )

    prompt = f"{system_prompt}\n\nChat History:\n{history_text}\nNew Query: {query}\n\nRewritten Query:"

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.0,
            max_tokens=100,
        )
        rewritten = chat_completion.choices[0].message.content.strip()
        # Clean up possible quotes if LLM added them
        if rewritten.startswith('"') and rewritten.endswith('"'):
            rewritten = rewritten[1:-1]
        elif rewritten.startswith("'") and rewritten.endswith("'"):
            rewritten = rewritten[1:-1]
            
        return rewritten
    except Exception as e:
        print(f"Error rewriting query: {e}")
        return query
