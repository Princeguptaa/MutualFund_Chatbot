from typing import List, Dict, Any
import json
import os
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

def retrieve(query: str, scheme_name: str = None, top_k: int = 30) -> List[Dict[str, Any]]:
    """
    Retrieves the most relevant chunks using TF-IDF and Cosine Similarity.
    """
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        store_path = os.path.join(base_dir, "data", "vectorstore", "tfidf_store.pkl")
        
        if not os.path.exists(store_path):
            st.error(f"TF-IDF store not found at {store_path}. Please run ingest_pipeline.py")
            print("TF-IDF store not found. Please run ingest_pipeline.py")
            return []
            
        with open(store_path, "rb") as f:
            store_data = pickle.load(f)
            
        vectorizer = store_data["vectorizer"]
        tfidf_matrix = store_data["tfidf_matrix"]
        chunks = store_data["chunks"]
        
        valid_urls = []
        if scheme_name and scheme_name.lower() != "unknown":
            sources_path = os.path.join(base_dir, "data", "sources.json")
            if os.path.exists(sources_path):
                with open(sources_path, 'r', encoding='utf-8') as f:
                    sources_data = json.load(f)
                    for s in sources_data:
                        if any(scheme_name.lower() in scheme.lower() for scheme in s.get("schemes", [])):
                            valid_urls.append(s["url"])
                            
            if not valid_urls:
                st.error(f"Scheme '{scheme_name}' not found in sources.json at {sources_path}.")
                # Scheme was parsed, but not in our sources.json! Out of scope.
                return []
                
        # Compute similarities
        query_vec = vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
        
        # Filter and sort
        scored_chunks = []
        for i, score in enumerate(similarities):
            # Only consider chunks with a non-zero similarity
            if score > 0:
                chunk = chunks[i]
                if valid_urls:
                    if chunk["metadata"].get("source_url") not in valid_urls:
                        continue
                        
                scored_chunks.append({
                    "text": chunk["text"],
                    "metadata": chunk["metadata"],
                    "distance": 1.0 - score  # 0 distance = exact match
                })
                
        # Sort by distance (lowest first, which means highest similarity)
        scored_chunks.sort(key=lambda x: x["distance"])
        return scored_chunks[:top_k]
        
    except Exception as e:
        st.error(f"Retrieval failed with exception: {str(e)}")
        print(f"Retrieval failed: {e}")
        return []

