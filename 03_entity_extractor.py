import re

# =====================================
# READ DOCUMENT
# =====================================

with open(
    "data/documents/sample.txt",
    "r",
    encoding="utf-8"
) as file:
    text = file.read()

print("\nDOCUMENT:")
print("=" * 50)
print(text)

# =====================================
# ENTITY EXTRACTION
# =====================================

entities = re.findall(
    r'\b[A-Z][a-zA-Z]+\b',
    text
)

entities = list(set(entities))

print("\nENTITIES FOUND")
print("=" * 50)

for entity in entities:
    print(entity)