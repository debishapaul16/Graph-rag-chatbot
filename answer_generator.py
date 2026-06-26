# ==========================================================
# IMPORT LIBRARIES
# ==========================================================

from config import llm
from hybrid_search import return_data

# ==========================================================
# LOAD GEMMA
# ==========================================================

print("Loading Gemma...")

llm = OllamaLLM(model="gemma3")

print("Gemma Loaded Successfully")

# ==========================================================
# GET DATA FROM HYBRID SEARCH
# ==========================================================

question = return_data["question"]

graph_context = return_data["graph_context"]

vector_context = return_data["vector_context"]

combined_context = return_data["combined_context"]

# ==========================================================
# CREATE PROMPT
# ==========================================================

prompt = f"""
You are an intelligent AI assistant.

Answer the user's question ONLY using the information
provided below.

If the answer is not present in the context,
reply exactly:

"I couldn't find the answer in the provided documents."

----------------------------------------

GRAPH CONTEXT

{graph_context}

----------------------------------------

VECTOR CONTEXT

{vector_context}

----------------------------------------

QUESTION

{question}

----------------------------------------

ANSWER
"""

# ==========================================================
# GENERATE ANSWER
# ==========================================================

print("\nGenerating Answer...\n")

answer = llm.invoke(prompt)

# ==========================================================
# DISPLAY ANSWER
# ==========================================================

print("=" * 60)
print("FINAL ANSWER")
print("=" * 60)

print(answer)
