from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

# create and set keyspace
keyspace_name = "upa"
session.execute(f'DROP KEYSPACE IF EXISTS {keyspace_name}')
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS %s
    WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '1' }
    """ % keyspace_name)
session.set_keyspace(keyspace_name)

session.execute("""
    CREATE TABLE mytable (
         text,
         text,
         text,
        PRIMARY KEY (thekey, col1)
    )
    """)

prepared = session.prepare("""
    INSERT INTO mytable (thekey, col1, col2)
    VALUES (?, ?, ?)
    """)

for i in range(10):
    session.execute(query, dict(key="key%d" % i, a='a', b='b'))
    session.execute(prepared.bind(("key%d" % i, 'b', 'b')))