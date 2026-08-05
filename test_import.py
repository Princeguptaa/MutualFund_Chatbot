import sys
import os
sys.path.insert(0, os.path.abspath("backend"))

try:
    from src.ingestion.ingest_pipeline import run_ingestion
    print("SUCCESS")
except Exception as e:
    import traceback
    traceback.print_exc()
