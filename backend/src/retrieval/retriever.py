from typing import List, Dict, Any
import json
import os
from src.vectorstore.chroma_client import get_chroma_client, get_collection

def retrieve(query: str, scheme_name: str = None, top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Retrieves the most relevant chunks using ChromaDB.
    """
    try:
        client = get_chroma_client()
        collection = get_collection(client)
        
        where_filter = None
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
            
            # If multiple URLs match, we can use $in operator
            if len(valid_urls) == 1:
                where_filter = {"source_url": valid_urls[0]}
            elif len(valid_urls) > 1:
                where_filter = {"source_url": {"$in": valid_urls}}
                
        results = collection.query(
            query_texts=[query],
            n_results=top_k,
            where=where_filter
        )
        
        retrieved_chunks = []
        if results and results.get("documents") and results["documents"][0]:
            for i in range(len(results["documents"][0])):
                doc_text = results["documents"][0][i]
                metadata = results["metadatas"][0][i] if results.get("metadatas") else {}
                distance = results["distances"][0][i] if results.get("distances") else 0.0
                
                retrieved_chunks.append({
                    "text": doc_text,
                    "metadata": metadata,
                    "distance": distance
                })
                
        return retrieved_chunks
    except Exception as e:
        print(f"Retrieval failed: {e}")
        return []

