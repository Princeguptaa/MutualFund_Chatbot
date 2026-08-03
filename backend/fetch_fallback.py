import json
import httpx
from bs4 import BeautifulSoup
import os

def extract_text(html):
    soup = BeautifulSoup(html, "html.parser")
    for element in soup(["script", "style", "nav", "footer", "header"]):
        element.decompose()
    return soup.get_text(separator="\n", strip=True)

with open("data/sources.json", "r") as f:
    sources = json.load(f)

docs = []
for source in sources:
    try:
        r = httpx.get(
            source['url'], 
            follow_redirects=True, 
            timeout=15, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        text = extract_text(r.text)
        
        # Groww 404 block check
        if "404! Page Not Found" in text and "groww.in" in source['url']:
            print(f"Skipping {source['url']} due to 404 bot block")
            continue
            
        docs.append({"url": source['url'], "text": text})
        print(f"Fetched {source['url']}, length: {len(text)}")
    except Exception as e:
        print(f"Error fetching {source['url']}: {e}")

with open("data/fallback_docs.json", "w", encoding="utf-8") as f:
    json.dump(docs, f, ensure_ascii=False, indent=2)
print("Saved to fallback_docs.json")
