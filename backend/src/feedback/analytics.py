import json
import os
from datetime import datetime
from typing import Dict, Any

ANALYTICS_FILE = "data/analytics/events.jsonl"

def log_event(event_type: str, fields: Dict[str, Any]):
    """
    Logs an analytics event to a JSON lines file.
    Event types: query_received, pii_blocked, refusal_served, answer_served, feedback_received
    """
    # Adjust path if running from deep directory
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    file_path = os.path.join(base_dir, ANALYTICS_FILE)
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    entry = {
        "event_type": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        **fields
    }
    
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
