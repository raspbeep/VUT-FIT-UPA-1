from neo4j import GraphDatabase
import pandas as pd

file_path = 'neo4j_financni_toky.csv'

df = pd.read_csv(file_path)

columns_to_keep = ['OBJECTID', 'NAZEV', 'OBEC', 'KRAJ', 'OKRES', 'DOTACE_CASTKA_UVOLNENA', 'DOTACE_CASTKA_CERPANA', 'DOTACE_FINANCNI_ZDROJ_NAZEV']
df = df[columns_to_keep]

df = df.dropna(subset=columns_to_keep)
df = df[~df.applymap(lambda x: isinstance(x, str) and x.strip() == '').any(axis=1)]

unique_nazev_count = df['NAZEV'].nunique()

print(f"Number of unique 'NAZEV' values: {unique_nazev_count}")
print(df.head()) 

uri = "bolt://localhost:7687"
username = "neo4j"
password = "password"

driver = GraphDatabase.driver(uri, auth=(username, password))

BATCH_SIZE = 5000 

def batch_insertion(data):
    with driver.session() as session:
        query = """
        UNWIND $data AS row
        MERGE (org:Organization {NAME: row.NAZEV})
        MERGE (region:Region {NAME: row.KRAJ})
        MERGE (district:District {NAME: row.OKRES, REGION: row.KRAJ})
        MERGE (city:City {NAME: row.OBEC, DISTRICT: row.OKRES, REGION: row.KRAJ})
        MERGE (gov:Government {NAME: row.DOTACE_FINANCNI_ZDROJ_NAZEV})
        MERGE (org)-[r:RECEIVED_FROM {allocated: row.DOTACE_CASTKA_UVOLNENA, used: row.DOTACE_CASTKA_CERPANA}]->(gov)
        MERGE (org)-[:LOCATED_IN]->(city)
        MERGE (city)-[:PART_OF]->(district)
        MERGE (district)-[:PART_OF]->(region)
        """
        session.run(query, data=data)

with driver.session() as session:
    session.run("MATCH (n) DETACH DELETE n")

data_list = df.to_dict(orient='records')

for i in range(0, len(data_list), BATCH_SIZE):
    batch = data_list[i:i+BATCH_SIZE]
    batch_insertion(batch)
driver.close()
