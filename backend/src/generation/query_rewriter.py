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
        "You are an expert AI assistant that rewrites follow-up questions to be standalone queries.\n"
        "Given the chat history and a new user query, rewrite the query to be standalone, "
        "replacing pronouns or contextual references (like 'it', 'this fund', 'that scheme') "
        "with the specific mutual fund or topic being discussed.\n\n"
        "EXAMPLES:\n"
        "History: User: What is the NAV of SBI Small Cap?\nAssistant: The NAV is 145.\n"
        "New Query: What is its expense ratio?\n"
        "Rewritten Query: What is the expense ratio of SBI Small Cap?\n\n"
        "History: User: Tell me about HDFC Flexi Cap.\nAssistant: It is a good fund.\n"
        "New Query: who manages it?\n"
        "Rewritten Query: Who manages HDFC Flexi Cap?\n\n"
        "IMPORTANT: Respond with ONLY the rewritten query text. Do not include any explanations, quotes, or conversational filler."
    )

    prompt = f"Chat History:\n{history_text}\nNew Query: {query}\n\nRewritten Query:"

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
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
