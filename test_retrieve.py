from src.retrieval.retriever import retrieve
print("Retrieving...")
try:
    chunks = retrieve("What is the exit load?")
    print("Chunks:", chunks)
except Exception as e:
    print("Exception:", e)
print("Done.")
