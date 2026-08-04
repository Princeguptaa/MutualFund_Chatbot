from typing import List, Dict, Any
import json
import os
import math
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.ingestion.chunker import chunk_text

_fallback_data = None
_vectorizer = None
_tfidf_matrix = None
_chunk_mapping = []

def _init_fallback():
    global _fallback_data, _vectorizer, _tfidf_matrix, _chunk_mapping
    if _fallback_data is not None:
        return

    _fallback_data = []
    _chunk_mapping = []
    
    # Load raw documents
    fallback_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "fallback_docs.json")
    if os.path.exists(fallback_path):
        with open(fallback_path, 'r', encoding='utf-8') as f:
            docs = json.load(f)
            
        for doc in docs:
            url = doc['url']
            text = doc['text']
            # Chunk the raw text
            chunks = chunk_text(text, chunk_size=300, chunk_overlap=50)
            for c in chunks:
                _fallback_data.append(c)
                _chunk_mapping.append({
                    "url": url,
                    "text": c
                })
    
    if _fallback_data:
        _vectorizer = TfidfVectorizer(stop_words='english')
        _tfidf_matrix = _vectorizer.fit_transform(_fallback_data)

def retrieve(query: str, scheme_name: str = None, top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Retrieves the most relevant chunks using a fallback TF-IDF search.
    """
    try:
        _init_fallback()
        
        if not _fallback_data or _vectorizer is None:
            raise ValueError("No fallback data loaded.")
            
        # Optional: Filter by scheme_name mapping
        valid_urls = None
        if scheme_name and scheme_name.lower() != "unknown":
            valid_urls = []
            sources_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "sources.json")
            if os.path.exists(sources_path):
                with open(sources_path, 'r', encoding='utf-8') as f:
                    sources_data = json.load(f)
                    for s in sources_data:
                        if any(scheme_name.lower() in scheme.lower() for scheme in s.get("schemes", [])):
                            valid_urls.append(s["url"])
                            
            if not valid_urls:
                # Scheme was parsed, but not in our sources.json! Out of scope.
                return []
            
        query_vec = _vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, _tfidf_matrix).flatten()
        
        # Get top_k indices
        top_indices = similarities.argsort()[::-1]
        
        retrieved_chunks = []
        for idx in top_indices:
            if len(retrieved_chunks) >= top_k:
                break
                
            score = similarities[idx]
            if score < 0.10: # Lower threshold to accommodate rewritten queries
                continue
                
            chunk_info = _chunk_mapping[idx]
            
            # Enforce scheme matching if applicable
            if valid_urls is not None and chunk_info["url"] not in valid_urls:
                continue
                
            retrieved_chunks.append({
                "text": chunk_info["text"],
                "metadata": {
                    "source_url": chunk_info["url"],
                    "doc_type": "fund_details",
                    "last_verified_date": "2024-03-01"
                },
                "distance": 1.0 - float(score) # Convert similarity to pseudo-distance
            })
            
        return retrieved_chunks
    except Exception as e:
        print(f"Fallback retrieval failed: {e}")
        return []
