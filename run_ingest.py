import sys
import os
sys.path.insert(0, os.path.abspath("backend"))

import asyncio
import traceback

from src.ingestion.ingest_pipeline import run_ingestion

async def main():
    try:
        await run_ingestion()
    except Exception as e:
        print("EXCEPTION OCCURRED:", e)
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
