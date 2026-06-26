from langchain_ollama import OllamaLLM
from neo4j import GraphDatabase
import json
import re

# =====================================
# NEO4J CONNECTION
# =====================================

URI = "bolt://172.26.0.1:7687"
USERNAME = "neo4j"
PASSWORD = "debishapaul16"

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

print("Connected To Neo4j")

# =====================================
# LOAD GEMMA
# =====================================

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

# =====================================
# PROMPT
# =====================================

prompt = f"""
Extract all entities and relationships.

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

response = llm.invoke(prompt)
print("\nRAW RESPONSE:")
print(response)

# =====================================
# REMOVE ```json ``` WRAPPERS
# =====================================

response = re.sub(r"```json", "", response)
response = re.sub(r"```", "", response)

# =====================================
# CONVERT JSON STRING TO PYTHON LIST
# =====================================

relationships = json.loads(response)

print("\nRelationships Found:\n")

for rel in relationships:
    print(rel)

# =====================================
# STORE IN NEO4J
# =====================================

with driver.session(database="gdb") as session:

    for rel in relationships:

        source = rel["source"]
        relation = rel["relationship"]
        target = rel["target"]

        query = f"""
        MERGE (a:Entity {{name:$source}})
        MERGE (b:Entity {{name:$target}})
        MERGE (a)-[:{relation}]->(b)
        """

        session.run(
            query,
            source=source,
            target=target
        )

print("\nGraph Created Successfully")

driver.close()