from langchain_ollama import OllamaLLM

# =====================================
# LOAD GEMMA
# =====================================

print("Loading Gemma...")

llm = OllamaLLM(model="gemma3")

print("Gemma Loaded")

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
# PROMPT GEMMA
# =====================================

prompt = f"""
You are an information extraction system.

Extract entities and relationships from the text.

Return ONLY JSON.

Format:

[
  {{
    "source":"Machine Learning",
    "relationship":"SUBSET_OF",
    "target":"Artificial Intelligence"
  }}
]

Text:

{text}
"""

print("\nSending to Gemma...\n")

response = llm.invoke(prompt)

print("=" * 50)
print("GEMMA OUTPUT")
print("=" * 50)

print(response)