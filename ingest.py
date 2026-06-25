from langchain_text_splitters import RecursiveCharacterTextSplitter

# Read document
with open("data/documents/sample.txt", "r", encoding="utf-8") as file:
    text = file.read()

print("=" * 50)
print("ORIGINAL DOCUMENT")
print("=" * 50)
print(text)

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