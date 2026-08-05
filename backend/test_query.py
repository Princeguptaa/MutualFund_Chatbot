import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.retrieval.query_preprocessor import preprocess_query
from src.retrieval.retriever import retrieve

queries = [
    "What is the exit load for SBI Small Cap Fund?",
    "What is the more about SBI Small Cap Fund?",
    "What is the more about SBI large Cap Fund?",
    "What is the more about SBI flexicap Fund?"
]

for q in queries:
    norm_q, scheme, clarif = preprocess_query(q)
    print(f"Query: {q}")
    print(f"Preprocessed: {norm_q} | Scheme: {scheme} | Clarif: {clarif}")
    chunks = retrieve(norm_q, scheme)
    print(f"Retrieved chunks: {len(chunks)}")
    if chunks:
        for c in chunks:
            print(f"  {c['metadata'].get('source_url')} | Distance: {c['distance']}")
    print("-" * 50)
