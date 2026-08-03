import json
import os
from datetime import datetime

FEEDBACK_FILE = "data/feedback/feedback.jsonl"

def store_feedback(query_hash: str, intent: str, answer_hash: str, feedback: str):
    """
    Stores user feedback in a JSON lines file.
    Does not store raw queries or PII.
    """
    # Adjust path if running from deep directory
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    file_path = os.path.join(base_dir, FEEDBACK_FILE)
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    entry = {
        "query_hash": query_hash,
        "intent": intent,
        "answer_hash": answer_hash,
        "feedback": feedback,  # "up" or "down"
        "timestamp": datetime.utcnow().isoformat()
    }
    
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
