import chromadb
from chromadb.config import Settings
import json
from src.vectorstore.chroma_client import DummyEmbeddingFunction

client = chromadb.PersistentClient(path="data/vectorstore", settings=Settings(anonymized_telemetry=False))
collection = client.get_or_create_collection(
    name="groww_rag_collection",
    embedding_function=DummyEmbeddingFunction()
)

print("Getting documents...")
all_docs = collection.get()

data = []
if all_docs and all_docs['documents']:
    for i in range(len(all_docs['documents'])):
        data.append({
            "text": all_docs['documents'][i],
            "metadata": all_docs['metadatas'][i]
        })

print(f"Found {len(data)} chunks. Saving to data.json")
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Done.")
