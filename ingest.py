from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb
# ==================================================
# STEP 1 : READ DOCUMENT
# ==================================================

with open("data/documents/sample.txt", "r", encoding="utf-8") as file:
    text = file.read()

print("=" * 50)
print("ORIGINAL DOCUMENT")
print("=" * 50)
print(text)

# ==================================================
# STEP 2 : CHUNKING
# ==================================================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20
)

chunks = splitter.split_text(text)

print("\n" + "=" * 50)
print("DOCUMENT CHUNKS")
print("=" * 50)

for i, chunk in enumerate(chunks, start=1):
    print(f"\nChunk {i}")
    print("-" * 30)
    print(chunk)

# ==================================================
# STEP 3 : LOAD EMBEDDING MODEL
# ==================================================

print("\nLoading Embedding Model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding Model Loaded Successfully")

# ==================================================
# STEP 4 : GENERATE EMBEDDINGS
# ==================================================

print("\nGenerating Embeddings...")

embeddings = model.encode(chunks)

print("Embeddings Generated Successfully")

# ==================================================
# STEP 5 : DISPLAY EMBEDDING INFORMATION
# ==================================================

print("\n" + "=" * 50)
print("EMBEDDING INFORMATION")
print("=" * 50)

print(f"\nTotal Chunks : {len(chunks)}")

print(f"Embedding Dimension : {len(embeddings[0])}")

print("\nFirst 10 values of Chunk 1 Embedding:")

print(embeddings[0][:10])

# ==================================================
# STEP 6 : SHOW CHUNK ↔ VECTOR RELATION
# ==================================================

print("\n" + "=" * 50)
print("CHUNK AND ITS EMBEDDING")
print("=" * 50)

for i in range(len(chunks)):
    print(f"\nChunk {i+1}:")
    print(chunks[i])

    print("\nVector (first 5 values):")
    print(embeddings[i][:5])

    print("-" * 50)
# ==================================================
# STEP 7 : CONNECT TO CHROMADB
# ==================================================

print("\n" + "=" * 50)
print("CONNECTING TO CHROMADB")
print("=" * 50)

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="documents"
)

print("ChromaDB Connected Successfully")
print("Collection Ready")

# ==================================================
# STEP 8 : STORE CHUNKS AND EMBEDDINGS
# ==================================================

print("\nStoring Data in ChromaDB...")

for i, chunk in enumerate(chunks):

    collection.add(
        ids=[f"chunk_{i}"],
        documents=[chunk],
        embeddings=[embeddings[i].tolist()]
    )

print("All Chunks Stored Successfully")

# ==================================================
# STEP 9 : VERIFY STORAGE
# ==================================================

print("\n" + "=" * 50)
print("VERIFYING CHROMADB STORAGE")
print("=" * 50)

print(f"Total Records Stored: {collection.count()}")

# Fetch first few records

results = collection.get()

print("\nStored IDs:")
print(results["ids"])

print("\nStored Documents:")

for doc in results["documents"]:
    print("-" * 30)
    print(doc)