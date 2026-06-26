from neo4j import GraphDatabase

URI = "bolt://172.26.0.1:7687"
USER = "neo4j"
PASSWORD = "debishapaul16"

driver = GraphDatabase.driver(
    URI,
    auth=(USER, PASSWORD)
)

try:
    driver.verify_connectivity()
    print("CONNECTED SUCCESSFULLY")

    with driver.session(database="gdb") as session:
        result = session.run("RETURN 'Neo4j Connected' AS msg")
        print(result.single()["msg"])

finally:
    driver.close()

