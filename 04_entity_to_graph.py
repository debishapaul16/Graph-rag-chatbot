import re
from neo4j import GraphDatabase

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

print("Connected to Neo4j")

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
# EXTRACT ENTITIES
# =====================================

entities = re.findall(
    r'\b[A-Z][a-zA-Z]+\b',
    text
)

entities = list(set(entities))

print("\nEntities Found:")
print(entities)

# =====================================
# STORE IN NEO4J
# =====================================

query = """
MERGE (e:Entity {name:$name})
"""

with driver.session(database="gdb") as session:

    for entity in entities:

        session.run(
            query,
            name=entity
        )

print("\nEntities Stored Successfully")

driver.close()