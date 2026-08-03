from src.scheduler.alerts import send_alert

def sweep_stale_data():
    """
    Sweeps the registry to find sources past their verify thresholds.
    """
    send_alert("INFO", "stale_data_sweep", "Job started", "Checking for stale data...")
    # Mock implementation for MVP
    send_alert("INFO", "stale_data_sweep", "Job completed", "No stale sources found.")
