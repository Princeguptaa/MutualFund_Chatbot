import re
from typing import List

def chunk_text(text: str, chunk_size: int = 300, chunk_overlap: int = 50) -> List[str]:
    """
    Chunks the input text using a simple character-based approach
    to avoid heavy dependencies like PyTorch on Windows.
    """
    if not text:
        return []
    
    # Very simple overlap-based chunking
    words = text.split()
    chunks = []
    
    # We approximate words to characters (avg 5 chars + 1 space = 6 chars per word)
    words_per_chunk = max(1, chunk_size // 6)
    overlap_words = max(1, chunk_overlap // 6)
    
    if len(words) <= words_per_chunk:
        return [text]
        
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + words_per_chunk])
        chunks.append(chunk)
        i += (words_per_chunk - overlap_words)
        
        # Prevent infinite loop if overlap >= words_per_chunk
        if words_per_chunk <= overlap_words:
            i += 1
            
    return chunks
