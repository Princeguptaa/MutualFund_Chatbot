import json
import uuid
import yaml
import os
import asyncio
from typing import List, Dict, Any

from playwright.async_api import async_playwright, BrowserContext
from src.ingestion.document_fetcher import fetch_html_async
from src.ingestion.html_parser import extract_text
from src.ingestion.chunker import chunk_text
from src.vectorstore.chroma_client import get_chroma_client, get_collection, get_config

def load_sources(filepath: str) -> List[Dict[str, Any]]:
    with open(filepath, 'r') as f:
        return json.load(f)

async def process_source(source, collection, chunk_size, chunk_overlap, semaphore, browser_context: BrowserContext):
    async with semaphore:
        url = source["url"]
        print(f"Processing URL: {url}")
        
        page = await browser_context.new_page()
        # 1. Fetch
        html = await fetch_html_async(url, page=page)
        await page.close()
        
        if not html:
            print(f"Failed to fetch {url}. Skipping.")
            return
            
        # 2. Parse
        text = extract_text(html)
        if not text:
            print(f"Failed to extract text from {url}. Skipping.")
            return
            
        # 3. Chunk
        chunks = chunk_text(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        print(f"Extracted {len(chunks)} chunks for {url}.")
        
        # 4. Prepare for vector store
        ids = []
        documents = []
        metadatas = []
        
        for i, chunk in enumerate(chunks):
            chunk_id = f"{url}-chunk-{i}"
            ids.append(chunk_id)
            documents.append(chunk)
            
            metadata = {
                "source_url": url,
                "doc_type": source.get("doc_type", "unknown"),
                "last_verified_date": source.get("last_verified", ""),
            }
            if "schemes" in source and isinstance(source["schemes"], list):
                metadata["schemes"] = ",".join(source["schemes"])
                
            metadatas.append(metadata)
            
        # 5. Upsert to ChromaDB
        if ids:
            try:
                collection.upsert(
                    ids=ids,
                    documents=documents,
                    metadatas=metadatas
                )
                print(f"Upserted {len(ids)} chunks to ChromaDB for {url}")
            except Exception as e:
                print(f"ChromaDB upsert failed for {url}: {e}")

async def run_ingestion():
    config = get_config()
    sources_file = config.get("source_registry_path", "data/sources.json")
    
    # Adjust path relative to project root
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    sources_file = os.path.join(base_dir, sources_file)
    
    sources = load_sources(sources_file)
    
    client = get_chroma_client()
    collection = get_collection(client)
    
    chunk_size = config.get("chunk_size", 300)
    chunk_overlap = config.get("chunk_overlap", 50)
    
    print(f"Loaded {len(sources)} sources for ingestion.")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        browser_context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        semaphore = asyncio.Semaphore(1) # limit concurrent requests to 1
        tasks = [process_source(source, collection, chunk_size, chunk_overlap, semaphore, browser_context) for source in sources]
        
        await asyncio.gather(*tasks)
        await browser.close()
    
    print("Ingestion pipeline completed.")
            
    print("Ingestion pipeline completed.")

if __name__ == "__main__":
    asyncio.run(run_ingestion())
