from neo4j import GraphDatabase

# ==================================================
# STEP 1 : CONNECT TO NEO4J
# ==================================================

URI = "bolt://172.26.0.1:7687"
USERNAME = "neo4j"
PASSWORD = "debishapaul16"

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

print("Connected to Neo4j")

# ==================================================
# STEP 2 : CREATE SAMPLE NODE
# ==================================================

query = """
CREATE (n:Technology {name:'Python'})
RETURN n
"""

with driver.session(database="gdb") as session:
    result = session.run(query)

print("Node Created Successfully")

driver.close()