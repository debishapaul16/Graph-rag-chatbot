# ==========================================================
# IMPORT LIBRARIES
# ==========================================================

from langchain_ollama import OllamaLLM
from sentence_transformers import SentenceTransformer
from neo4j import GraphDatabase
import chromadb

# ==========================================================
# LOAD GEMMA
# ==========================================================

print("Loading Gemma...")

llm = OllamaLLM(model="gemma3")

print("Gemma Ready")

# ==========================================================
# LOAD EMBEDDING MODEL
# ==========================================================

print("Loading Embedding Model...")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Embedding Model Ready")

# ==========================================================
# CONNECT NEO4J
# ==========================================================

URI = "bolt://172.26.0.1:7687"

USERNAME = "neo4j"

PASSWORD = "debishapaul16"

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

print("Neo4j Connected")

# ==========================================================
# CONNECT CHROMADB
# ==========================================================

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_collection(
    "documents"
)

print("ChromaDB Connected")