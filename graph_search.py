from neo4j import GraphDatabase

# =====================================
# CONNECT TO NEO4J
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
# USER INPUT
# =====================================

entity = input("Enter Entity: ")

# =====================================
# QUERY
# =====================================

query = """
MATCH (a)-[r]->(b)
WHERE toLower(b.name) = toLower($entity)

RETURN
a.name AS source,
type(r) AS relationship,
b.name AS target
"""

# =====================================
# SEARCH GRAPH
# =====================================

with driver.session(database="gdb") as session:

    result = session.run(
        query,
        entity=entity
    )

    print("\nResults")
    print("=" * 50)

    found = False

    for record in result:

        found = True

        print(
            f"{record['source']} "
            f"--{record['relationship']}--> "
            f"{record['target']}"
        )

    if not found:
        print("No relationships found")

driver.close()