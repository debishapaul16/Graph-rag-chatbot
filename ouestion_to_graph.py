from langchain_ollama import OllamaLLM
from neo4j import GraphDatabase

# =====================================
# GEMMA
# =====================================

llm = OllamaLLM(model="gemma3")

# =====================================
# NEO4J
# =====================================

URI = "bolt://172.26.0.1:7687"
USERNAME = "neo4j"
PASSWORD = "debishapaul16"

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

print("System Ready")

# =====================================
# USER QUESTION
# =====================================

question = input("\nAsk Question: ")

# =====================================
# ENTITY EXTRACTION
# =====================================

prompt = f"""
Extract ONLY the main entity.

Question:
{question}

Return only entity name.
"""

entity = llm.invoke(prompt).strip()

print("\nEntity Found:")
print(entity)

# =====================================
# GRAPH SEARCH
# =====================================

query = """
MATCH (a)-[r]->(b)
WHERE toLower(b.name)=toLower($entity)

RETURN
a.name AS source,
type(r) AS relation,
b.name AS target
"""

with driver.session(database="gdb") as session:

    result = session.run(
        query,
        entity=entity
    )

    print("\nGraph Context")
    print("="*50)

    found = False

    for record in result:

        found = True

        print(
            f"{record['source']} "
            f"--{record['relation']}--> "
            f"{record['target']}"
        )

    if not found:
        print("Nothing Found")

driver.close()