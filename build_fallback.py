import os
import json
import asyncio
from playwright.async_api import async_playwright

async def fetch_html_async(url: str, page) -> str:
    print(f"Fetching {url}")
    await page.goto(url, wait_until="networkidle", timeout=60000)
    await page.wait_for_timeout(2000)
    
    # Optional: scroll to trigger lazy loading
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    await page.wait_for_timeout(1000)
    
    return await page.content()

from bs4 import BeautifulSoup
import re

def extract_text(html_content: str) -> str:
    soup = BeautifulSoup(html_content, 'html.parser')
    for element in soup(["script", "style", "noscript", "iframe"]):
        element.extract()
    text = soup.get_text(separator=' ', strip=True)
    text = re.sub(r'\s+', ' ', text)
    return text

async def build_fallback():
    base_dir = os.path.dirname(__file__)
    sources_path = os.path.join(base_dir, "backend", "data", "sources.json")
    with open(sources_path, 'r') as f:
        sources = json.load(f)
        
    fallback_data = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        browser_context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        for source in sources:
            url = source["url"]
            try:
                page = await browser_context.new_page()
                html = await fetch_html_async(url, page)
                await page.close()
                text = extract_text(html)
                fallback_data.append({
                    "url": url,
                    "text": text
                })
                print(f"Success: {url}")
            except Exception as e:
                print(f"Failed {url}: {e}")
                
        await browser.close()
        
    fallback_path = os.path.join(base_dir, "backend", "data", "fallback_docs.json")
    with open(fallback_path, 'w', encoding='utf-8') as f:
        json.dump(fallback_data, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(fallback_data)} docs to {fallback_path}")

if __name__ == "__main__":
    asyncio.run(build_fallback())
