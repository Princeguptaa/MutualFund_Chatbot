import httpx
from typing import Optional

async def fetch_html_async(url: str, timeout: int = 10) -> Optional[str]:
    """
    Fetches the HTML content from the given URL asynchronously.
    Returns the HTML text if successful, else None.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=timeout, follow_redirects=True)
            response.raise_for_status()
            return response.text
        except httpx.RequestError as e:
            print(f"Request error for {url}: {e}")
            return None
        except httpx.HTTPStatusError as e:
            print(f"HTTP error {e.response.status_code} for {url}: {e}")
            return None
