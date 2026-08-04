import os
from enum import Enum
from groq import Groq
from dotenv import load_dotenv
import logging
from src.data.alias_map import ALIAS_MAP

load_dotenv()

class Intent(Enum):
    FACTUAL = "FACTUAL"
    ADVISORY_OPINION = "ADVISORY_OPINION"
    PERFORMANCE_COMPARISON = "PERFORMANCE_COMPARISON"
    PII_CONTAINING = "PII_CONTAINING"
    OUT_OF_CORPUS = "OUT_OF_CORPUS"

def check_out_of_corpus(query: str) -> bool:
    query_lower = query.lower()
    # If it mentions "fund" or "scheme", check if it matches any alias.
    if "fund" in query_lower or "scheme" in query_lower:
        # Simplistic check: if it mentions a fund but doesn't match our alias map, it might be out of corpus.
        # This is a heuristic.
        for alias in ALIAS_MAP.keys():
            if alias in query_lower:
                return False # Found in corpus
        # If it specifically mentions something like "axis" or "parag parikh"
        out_of_corpus_keywords = ["axis", "parag parikh", "quant", "zerodha", "uti"]
        if any(kw in query_lower for kw in out_of_corpus_keywords):
            return True
    return False

def classify_intent_heuristic(query: str) -> Intent:
    """Fallback keyword heuristics."""
    if check_out_of_corpus(query):
        return Intent.OUT_OF_CORPUS
        
    query_lower = query.lower()
    advisory_keywords = ["should i", "recommend", "suggest", "which is better", "hypothetically", "if you were an advisor", "good time to invest", "where to invest"]
    if any(kw in query_lower for kw in advisory_keywords):
        return Intent.ADVISORY_OPINION
    performance_keywords = ["returns", "cagr", "compare performance", "5-year return", "annualised", "which gave more", "will it go up", "future return"]
    if any(kw in query_lower for kw in performance_keywords):
        return Intent.PERFORMANCE_COMPARISON
    return Intent.FACTUAL

def classify_intent(query: str) -> Intent:
    """
    Classifies the intent using Groq LLM, falls back to heuristic if API fails.
    """
    if check_out_of_corpus(query):
        return Intent.OUT_OF_CORPUS

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return classify_intent_heuristic(query)
        
    client = Groq(api_key=api_key)
    prompt = f"""Classify this user query into exactly one of these categories:
FACTUAL: Seeking information, facts, procedures, definitions, or status.
ADVISORY_OPINION: Asking for investment advice, recommendations, opinions on whether to buy/sell/hold, or which fund is "good" or "best".
PERFORMANCE_COMPARISON: Asking to compare returns, CAGR, or historical performance between funds.

Reply with ONLY the exact category name.
Query: {query}
Intent:"""

    try:
        chat = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.0,
            max_tokens=10,
        )
        result = chat.choices[0].message.content.strip().upper()
        if "ADVISORY" in result: return Intent.ADVISORY_OPINION
        if "PERFORMANCE" in result: return Intent.PERFORMANCE_COMPARISON
        return Intent.FACTUAL
    except Exception as e:
        logging.error(f"LLM intent classifier failed: {e}")
        return classify_intent_heuristic(query)

