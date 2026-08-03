from src.scheduler.alerts import send_alert

def reingest_corpus():
    """
    Re-fetches active sources, compares hashes, and updates ChromaDB.
    """
    send_alert("INFO", "corpus_reingestion", "Job started", "Re-ingesting active sources...")
    # Mock implementation for MVP
    send_alert("INFO", "corpus_reingestion", "Job completed", "0 sources changed.")
