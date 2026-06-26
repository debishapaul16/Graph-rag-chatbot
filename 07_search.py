import chromadb
from sentence_transformers import SentenceTransformer

# ==================================================
# STEP 1 : CONNECT TO CHROMADB
# ==================================================

print("Connecting to ChromaDB...")

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_collection("documents")

print("Connected Successfully")

# ==================================================
# STEP 2 : LOAD EMBEDDING MODEL
# ==================================================

print("Loading Embedding Model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model Loaded")

# ==================================================
# STEP 3 : USER QUESTION
# ==================================================

question = input("\nAsk a Question: ")

# ==================================================
# STEP 4 : CONVERT QUESTION TO VECTOR
# ==================================================

question_embedding = model.encode(question)

print("\nQuestion Converted To Embedding")

# ==================================================
# STEP 5 : SEARCH CHROMADB
# ==================================================

results = collection.query(
    query_embeddings=[question_embedding.tolist()],
    n_results=3
)

# ==================================================
# STEP 6 : DISPLAY RESULTS
# ==================================================

print("\n" + "=" * 50)
print("MOST RELEVANT CHUNKS")
print("=" * 50)

for i, doc in enumerate(results["documents"][0], start=1):
    print(f"\nResult {i}")
    print("-" * 30)
    print(doc)