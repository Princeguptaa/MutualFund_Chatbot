import chromadb
from chromadb.config import Settings
import hashlib
from chromadb.api.types import EmbeddingFunction, Documents, Embeddings

class DummyEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []
        for text in input:
            h = int(hashlib.md5(text.encode('utf-8')).hexdigest(), 16)
            vec = [float((h >> (i % 64)) & 1) for i in range(384)]
            embeddings.append(vec)
        return embeddings

print("Initializing client...")
client = chromadb.PersistentClient(path="data/vectorstore", settings=Settings(anonymized_telemetry=False))
print("Getting collection...")
collection = client.get_or_create_collection(
    name="groww_rag_collection",
    embedding_function=DummyEmbeddingFunction()
)
print("Querying...")
results = collection.query(
    query_texts=["What is the minimum SIP amount?"],
    n_results=1
)
print("Results:", results)
print("Done.")
