import json
import uuid
import yaml
import os
import asyncio
import pickle
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer

from playwright.async_api import async_playwright, BrowserContext
from src.ingestion.document_fetcher import fetch_html_async
from src.ingestion.html_parser import extract_text
from src.ingestion.chunker import chunk_text
from src.vectorstore.chroma_client import get_config

def load_sources(filepath: str) -> List[Dict[str, Any]]:
    with open(filepath, 'r') as f:
        return json.load(f)

async def process_source(source, chunk_size, chunk_overlap, semaphore, browser_context: BrowserContext):
    async with semaphore:
        url = source["url"]
        print(f"Processing URL: {url}")
        
        page = await browser_context.new_page()
        html = await fetch_html_async(url, page=page)
        await page.close()
        
        if not html:
            print(f"Failed to fetch {url}. Skipping.")
            return []
            
        text = extract_text(html)
        if not text:
            print(f"Failed to extract text from {url}. Skipping.")
            return []
            
        chunks = chunk_text(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        print(f"Extracted {len(chunks)} chunks for {url}.")
        
        results = []
        for i, chunk in enumerate(chunks):
            metadata = {
                "source_url": url,
                "doc_type": source.get("doc_type", "unknown"),
                "last_verified_date": source.get("last_verified", ""),
            }
            if "schemes" in source and isinstance(source["schemes"], list):
                metadata["schemes"] = ",".join(source["schemes"])
                
            results.append({
                "id": f"{url}-chunk-{i}",
                "text": chunk,
                "metadata": metadata
            })
            
        return results

async def run_ingestion():
    config = get_config()
    sources_file = config.get("source_registry_path", "data/sources.json")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    sources_file = os.path.join(base_dir, sources_file)
    
    sources = load_sources(sources_file)
    
    chunk_size = config.get("chunk_size", 300)
    chunk_overlap = config.get("chunk_overlap", 50)
    
    print(f"Loaded {len(sources)} sources for ingestion.")
    
    all_chunks = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        browser_context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        semaphore = asyncio.Semaphore(1)
        tasks = [process_source(source, chunk_size, chunk_overlap, semaphore, browser_context) for source in sources]
        
        results = await asyncio.gather(*tasks)
        for res in results:
            if res:
                all_chunks.extend(res)
                
        await browser.close()
    
    if not all_chunks:
        print("No chunks extracted. Exiting.")
        return
        
    print(f"Total {len(all_chunks)} chunks collected. Building TF-IDF vector store...")
    
    texts = [chunk["text"] for chunk in all_chunks]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)
    
    store_data = {
        "vectorizer": vectorizer,
        "tfidf_matrix": tfidf_matrix,
        "chunks": all_chunks
    }
    
    vectorstore_dir = os.path.join(base_dir, "data", "vectorstore")
    os.makedirs(vectorstore_dir, exist_ok=True)
    store_path = os.path.join(vectorstore_dir, "tfidf_store.pkl")
    
    with open(store_path, "wb") as f:
        pickle.dump(store_data, f)
        
    print(f"Saved TF-IDF store to {store_path}")
    print("Ingestion pipeline completed.")

if __name__ == "__main__":
    asyncio.run(run_ingestion())
