# ==========================================================
# IMPORT LIBRARIES
# ==========================================================

from langchain_ollama import OllamaLLM
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
import chromadb


# ==========================================================
# HYBRID SEARCH FUNCTION
# ==========================================================

def hybrid_search():

    # ==========================================================
    # STEP 1 : LOAD GEMMA MODEL
    # ==========================================================

    print("Loading Gemma...")

    llm = OllamaLLM(model="gemma3")

    print("Gemma Loaded Successfully")


    # ==========================================================
    # STEP 2 : CONNECT TO NEO4J
    # ==========================================================

    URI = "bolt://172.26.0.1:7687"
    USERNAME = "neo4j"
    PASSWORD = "debishapaul16"

    driver = GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD)
    )

    print("Connected To Neo4j")


    # ==========================================================
    # STEP 3 : LOAD EMBEDDING MODEL
    # ==========================================================

    print("Loading Embedding Model...")

    embedding_model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    print("Embedding Model Loaded")


    # ==========================================================
    # STEP 4 : CONNECT TO CHROMADB
    # ==========================================================

    client = chromadb.PersistentClient(path="chroma_db")

    collection = client.get_collection("documents")

    print("Connected To ChromaDB")


    # ==========================================================
    # STEP 5 : TAKE USER QUESTION
    # ==========================================================

    print()

    question = input("Ask your question : ")


    # ==========================================================
    # STEP 6 : EXTRACT ENTITY USING GEMMA
    # ==========================================================

    prompt = f"""
Extract the main entity from the question.

Question:
{question}

Return ONLY the entity.

No explanation.
"""

    entity = llm.invoke(prompt).strip()

    print("\nEntity Found :")
    print(entity)


    # ==========================================================
    # STEP 7 : GRAPH SEARCH
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

    print("\n" + "=" * 50)
    print("GRAPH CONTEXT")
    print("=" * 50)

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
    # STEP 8 : GENERATE QUESTION EMBEDDING
    # ==========================================================

    print("\nGenerating Question Embedding...")

    question_embedding = embedding_model.encode(question)

    print("Embedding Generated Successfully")


    # ==========================================================
    # STEP 9 : SEARCH CHROMADB
    # ==========================================================

    results = collection.query(
        query_embeddings=[question_embedding.tolist()],
        n_results=3
    )


    # ==========================================================
    # STEP 10 : VECTOR SEARCH
    # ==========================================================

    print("\n" + "=" * 50)
    print("VECTOR CONTEXT")
    print("=" * 50)

    vector_context = ""

    documents = results["documents"][0]

    for i, doc in enumerate(documents, start=1):

        print(f"\nChunk {i}")
        print("-" * 30)
        print(doc)

        vector_context += doc + "\n\n"


    # ==========================================================
    # STEP 11 : COMBINE CONTEXT
    # ==========================================================

    combined_context = f"""
================ GRAPH CONTEXT ================

{graph_context}

================ VECTOR CONTEXT ================

{vector_context}
"""


    print("\n" + "=" * 50)
    print("COMBINED CONTEXT")
    print("=" * 50)

    print(combined_context)


    # ==========================================================
    # STEP 12 : CLOSE CONNECTION
    # ==========================================================

    driver.close()

    print("\nNeo4j Connection Closed")


    # ==========================================================
    # RETURN EVERYTHING
    # ==========================================================

    return {
        "question": question,
        "entity": entity,
        "graph_context": graph_context,
        "vector_context": vector_context,
        "combined_context": combined_context
    }


# ==========================================================
# MAIN FUNCTION
# ==========================================================

if __name__ == "__main__":

    data = hybrid_search()

    print("\nReturned Successfully")