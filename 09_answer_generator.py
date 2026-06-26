# ==========================================================
# IMPORTS
# ==========================================================

from config import llm
from hybrid_search import hybrid_search


# ==========================================================
# ANSWER GENERATION FUNCTION
# ==========================================================

def generate_answer():

    # ==========================================================
    # STEP 1 : RETRIEVE CONTEXT
    # ==========================================================

    data = hybrid_search()

    question = data["question"]
    graph_context = data["graph_context"]
    vector_context = data["vector_context"]

    # ==========================================================
    # STEP 2 : BUILD PROMPT
    # ==========================================================

    prompt = f"""
You are an expert AI assistant.

Your job is to answer the user's question by combining information from BOTH the Graph Context and the Vector Context.

Instructions:

1. Read the complete Graph Context.
2. Read the complete Vector Context.
3. Combine information from multiple pieces of context.
4. Use graph relationships to improve your explanation.
5. Use information from BOTH contexts whenever possible.
6. Write the answer in your own words instead of copying sentences.
7. If multiple facts are related, connect them logically.
8. Give a detailed but concise explanation.
9. If the answer cannot be found, reply exactly:
"I couldn't find the answer in the provided documents."

--------------------------------------------------

GRAPH CONTEXT

{graph_context}

--------------------------------------------------

VECTOR CONTEXT

{vector_context}

--------------------------------------------------

QUESTION

{question}

--------------------------------------------------

FINAL ANSWER:
"""

    # ==========================================================
    # STEP 3 : GENERATE ANSWER
    # ==========================================================

    print("\nGenerating Answer...\n")

    answer = llm.invoke(prompt)

    # ==========================================================
    # STEP 4 : RETURN ANSWER
    # ==========================================================

    return answer


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    answer = generate_answer()

    print("\n")
    print("=" * 60)
    print("FINAL ANSWER")
    print("=" * 60)

    print(answer)