from neo4j import GraphDatabase

try:
    driver = GraphDatabase.driver(
        "bolt://172.26.0.1:7687",
        auth=("neo4j", "paul.debisha@2004")
    )

    driver.verify_connectivity()
    print("CONNECTED SUCCESSFULLY")

except Exception as e:
    print("ERROR:")
    print(e)

finally:
    try:
        driver.close()
    except:
        pass
