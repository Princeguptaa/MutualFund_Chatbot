from typing import Optional
from playwright.async_api import Page, Error as PlaywrightError

async def fetch_html_async(url: str, page: Page, timeout: int = 60000) -> Optional[str]:
    """
    Fetches the fully-rendered HTML content from the given URL using Playwright.
    Returns the HTML text if successful, else None.
    """
    try:
        await page.goto(url, timeout=timeout, wait_until="domcontentloaded")
        # Give it a tiny extra sleep to ensure React/JS finishes rendering numbers
        await page.wait_for_timeout(5000)
        content = await page.content()
        return content
    except PlaywrightError as e:
        print(f"Playwright error for {url}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error for {url}: {e}")
        return None
