# ==========================================================
# IMPORT SHARED OBJECTS
# ==========================================================

from config import llm
from config import embedding_model
from config import driver
from config import collection


# ==========================================================
# HYBRID SEARCH FUNCTION
# ==========================================================

def hybrid_search():

    # ==========================================================
    # STEP 1 : TAKE USER QUESTION
    # ==========================================================

    print("\n" + "=" * 60)
    print("HYBRID SEARCH")
    print("=" * 60)

    question = input("Ask your question : ")

    # ==========================================================
    # STEP 2 : EXTRACT ENTITY
    # ==========================================================

    prompt = f"""
Extract the main entity from the question.

Question:
{question}

Return ONLY the entity.

No explanation.
"""

    entity = llm.invoke(prompt).strip()

    print("\nEntity Found:")
    print(entity)

    # ==========================================================
    # STEP 3 : SEARCH KNOWLEDGE GRAPH
    # ==========================================================

    graph_query = """
    MATCH (a)-[r]->(b)
    WHERE toLower(a.name)=toLower($entity)
       OR toLower(b.name)=toLower($entity)

    RETURN
        a.name AS source,
        type(r) AS relationship,
        b.name AS target
    """

    graph_context = ""

    print("\n" + "=" * 60)
    print("GRAPH CONTEXT")
    print("=" * 60)

    with driver.session(database="gdb") as session:

        result = session.run(
            graph_query,
            entity=entity
        )

        found = False

        for record in result:

            found = True

            relation = (
                f"{record['source']} "
                f"--{record['relationship']}--> "
                f"{record['target']}"
            )

            print(relation)

            graph_context += relation + "\n"

        if not found:

            print("No Graph Information Found")

    # ==========================================================
    # STEP 4 : QUESTION EMBEDDING
    # ==========================================================

    print("\nGenerating Question Embedding...")

    question_embedding = embedding_model.encode(question)

    print("Embedding Generated Successfully")

    # ==========================================================
    # STEP 5 : VECTOR SEARCH
    # ==========================================================

    results = collection.query(

        query_embeddings=[
            question_embedding.tolist()
        ],

        n_results=3

    )

    # ==========================================================
    # STEP 6 : DISPLAY VECTOR CONTEXT
    # ==========================================================

    print("\n" + "=" * 60)
    print("VECTOR CONTEXT")
    print("=" * 60)

    vector_context = ""

    documents = results["documents"][0]

    for i, doc in enumerate(documents, start=1):

        print(f"\nChunk {i}")
        print("-" * 30)
        print(doc)

        vector_context += doc + "\n\n"

    # ==========================================================
    # STEP 7 : COMBINE CONTEXT
    # ==========================================================

    combined_context = f"""
================ GRAPH CONTEXT ================

{graph_context}

================ VECTOR CONTEXT ================

{vector_context}
"""

    print("\n" + "=" * 60)
    print("COMBINED CONTEXT")
    print("=" * 60)

    print(combined_context)

    # ==========================================================
    # STEP 8 : RETURN EVERYTHING
    # ==========================================================

    return {

        "question": question,

        "entity": entity,

        "graph_context": graph_context,

        "vector_context": vector_context,

        "combined_context": combined_context

    }


# ==========================================================
# RUN ONLY IF EXECUTED DIRECTLY
# ==========================================================

if __name__ == "__main__":

    data = hybrid_search()

    print("\n")
    print("=" * 60)
    print("RETURNED DATA")
    print("=" * 60)

    print(f"Question : {data['question']}")
    print(f"Entity   : {data['entity']}")