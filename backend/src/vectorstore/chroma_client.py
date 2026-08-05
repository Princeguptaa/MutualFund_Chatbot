import chromadb
from chromadb.config import Settings
import yaml
from typing import Dict, Any
import os
from chromadb.utils import embedding_functions

def get_embedding_function():
    return embedding_functions.DefaultEmbeddingFunction()

def get_config() -> Dict[str, Any]:
    config_path = 'config.yaml'
    if not os.path.exists(config_path):
        config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_chroma_client():
    config = get_config()
    persist_dir = config.get("chroma_persist_directory", "data/vectorstore/")
    if not os.path.isabs(persist_dir):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        persist_dir = os.path.join(base_dir, persist_dir)
    client = chromadb.PersistentClient(path=persist_dir, settings=Settings(anonymized_telemetry=False))
    return client

def get_collection(client):
    embedding_fn = get_embedding_function()
    collection = client.get_or_create_collection(
        name="groww_rag_collection",
        embedding_function=embedding_fn
    )
    return collection
