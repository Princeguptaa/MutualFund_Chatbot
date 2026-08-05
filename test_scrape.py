import asyncio
import sys
sys.path.append(r"c:\Users\Prince Gupta\.antigravity-ide\Groww_Rag")
from backend.src.ingestion.document_fetcher import fetch_html_async
from backend.src.ingestion.html_parser import extract_text
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        html = await fetch_html_async('https://www.sbimf.com/sbimf-scheme-details/sbi-small-cap-fund-329', page)
        text = extract_text(html)
        print("Scraped text length:", len(text) if text else 0)
        with open("out.txt", "w", encoding="utf-8") as f:
            f.write(text if text else "")
        with open("raw.html", "w", encoding="utf-8") as f:
            f.write(html if html else "")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test())
