import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    return _client

def generate_answer(prompt: str) -> str:
    """
    Calls the Groq API to generate an answer based on the prompt.
    """
    client = _get_client()
    
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant", # Groq model
        temperature=0.0,
        max_tokens=200,
    )
    return chat_completion.choices[0].message.content

def generate_answer_stream(prompt: str):
    """
    Yields chunks of the answer for streaming.
    """
    client = _get_client()
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
        temperature=0.0,
        max_tokens=200,
        stream=True
    )
    for chunk in chat_completion:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content
