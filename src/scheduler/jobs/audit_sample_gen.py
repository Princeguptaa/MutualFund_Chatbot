import json
import os
import random
from datetime import datetime

ANALYTICS_FILE = "data/analytics/events.jsonl"
AUDITS_DIR = "data/audits/"

def generate_audit_sample():
    """
    Generates an audit sample of 20 random queries from the past 7 days.
    Output: data/audits/audit_YYYY-WNN.json
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    analytics_path = os.path.join(base_dir, ANALYTICS_FILE)
    audits_dir_path = os.path.join(base_dir, AUDITS_DIR)
    
    if not os.path.exists(analytics_path):
        return
        
    os.makedirs(audits_dir_path, exist_ok=True)
    
    eligible_events = []
    with open(analytics_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                event = json.loads(line)
                if event.get("event_type") == "answer_served":
                    eligible_events.append(event)
            except:
                pass
                
    # Sample up to 20
    sample_size = min(20, len(eligible_events))
    sample = random.sample(eligible_events, sample_size)
    
    week_str = datetime.utcnow().strftime("%Y-W%W")
    audit_file = os.path.join(audits_dir_path, f"audit_{week_str}.json")
    
    with open(audit_file, "w", encoding="utf-8") as f:
        json.dump({"week": week_str, "sample_size": sample_size, "events": sample}, f, indent=2)
        
if __name__ == "__main__":
    generate_audit_sample()
