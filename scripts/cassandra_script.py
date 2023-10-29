from datetime import datetime
import geojson

from cassandra.cluster import Cluster
from cassandra.query import UNSET_VALUE

class Measurement:
    def __init__(self, objectid, code, name, owner, lat, lon, actualized, so2_1h, no2_1h,
                co_8h, pm10_1h, o3_1h, pm10_24h, pm2_5_1h, globalid):
        self.objectid = objectid
        self.code = code
        self.name = name
        self.owner = owner
        self.lat = lat
        self.lon = lon
        self.actualized = actualized
        self.so2_1h = so2_1h
        self.no2_1h = no2_1h
        self.co_8h = co_8h
        self.pm10_1h = pm10_1h
        self.o3_1h = o3_1h
        self.pm10_24h = pm10_24h
        self.pm2_5_1h = pm2_5_1h
        self.globalid = globalid


measurements = []

def load_dataset():
    with open("./cassandra_kvalita_ovzdusi.geojson", "r") as f:
        geojson_data = geojson.load(f)
        for measurement in geojson_data["features"]:
            mdict = measurement["properties"]
            m = Measurement(
                mdict["objectid"],
                mdict["code"],
                mdict["name"],
                mdict["owner"],
                float(mdict["lat"]),
                float(mdict["lon"]),
                datetime.fromisoformat(mdict["actualized"]),
                UNSET_VALUE if mdict["so2_1h"] is None else float(mdict["so2_1h"]),
                UNSET_VALUE if mdict["no2_1h"] is None else float(mdict["no2_1h"]),
                UNSET_VALUE if mdict["co_8h"] is None else float(mdict["co_8h"]),
                UNSET_VALUE if mdict["pm10_1h"] is None else float(mdict["pm10_1h"]),
                UNSET_VALUE if mdict["o3_1h"] is None else float(mdict["o3_1h"]),
                UNSET_VALUE if mdict["pm10_24h"] is None else float(mdict["pm10_24h"]),
                UNSET_VALUE if mdict["pm2_5_1h"] is None else float(mdict["pm2_5_1h"]),
                mdict["globalid"]
            )
            measurements.append(m)

cluster = Cluster(['127.0.0.1'])
session = cluster.connect()


keyspace_name = "upa"
def drop_keyspace():
    global session
    session.execute(f'DROP KEYSPACE IF EXISTS {keyspace_name}')

def create_and_set_keyspace():
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS %s
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '1' }
        """ % keyspace_name)
    session.set_keyspace(keyspace_name)

def create_table():
    session.execute("""
        CREATE TABLE measurements (
            objectid    int,
            code        text,
            name        text,
            owner       text,
            lat         float,
            lon         float,
            actualized  timestamp,
            so2_1h      float,
            no2_1h      float,
            co_8h       float,
            pm10_1h     float,
            o3_1h       float,
            pm10_24h    float,
            pm2_5_1h    float,
            globalid    text,
            PRIMARY KEY ((name, code), actualized, objectid)
        )
        """)

def prepare_statement():
    global prepared
    prepared = session.prepare("""
        INSERT INTO measurements (objectid, code, name, owner, lat, lon, actualized, so2_1h, no2_1h,
                                    co_8h, pm10_1h, o3_1h, pm10_24h, pm2_5_1h, globalid)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """)

def insert_data():
    print('inserting data...')
    for ms in measurements:
        session.execute(prepared.bind(values=vars(ms)))
    print('done')


def update_data():
    session.execute("UPDATE upa.measurements SET so2_1h = 42.0, no2_1h = 42.0 WHERE name = 'Brno-Svatoplukova' AND code='BBMSA' AND objectid = 97368 AND actualized = '2022-10-22 07:30:56.000000+0000'")

load_dataset()
drop_keyspace()
create_and_set_keyspace()
create_table()
prepare_statement()
insert_data()

update_data()
