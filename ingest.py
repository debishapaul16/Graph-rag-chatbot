from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

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