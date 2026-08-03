import trafilatura
from bs4 import BeautifulSoup
from typing import Optional

def extract_text(html_content: str) -> Optional[str]:
    """
    Extracts plain text from HTML content using trafilatura.
    Falls back to BeautifulSoup if trafilatura fails.
    """
    if not html_content:
        return None
        
    text = trafilatura.extract(html_content, include_comments=False, include_tables=True, no_fallback=False)
    
    if not text:
        # Fallback to BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text(separator=' ', strip=True)
        
    return text if text else None
