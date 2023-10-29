import pandas as pd
from influxdb_client import InfluxDBClient, Point, WritePrecision, QueryApi
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import BucketsApi

import random
from datetime import datetime, timedelta

df = pd.read_csv('nehody.csv', low_memory=False)

columns_to_keep = ['id', 'usmrceno_os', 'tezce_zran_os', 'lehce_zran_os', 'hmotna_skoda', 'datum']

df = df[columns_to_keep]

df.dropna(inplace=True)

df.drop_duplicates(subset='id', keep='first', inplace=True)

df.sort_values(by='datum', inplace=True)

df_grouped = df.groupby('datum').agg({
    'usmrceno_os': 'sum',
    'tezce_zran_os': 'sum',
    'lehce_zran_os': 'sum',
    'hmotna_skoda': 'sum'
}).reset_index()

token = "IiWPiC8sV5Uq6RPRGye_kJ2IXYiu_bp2UMN3cktXm-bj-FQuT9-STqHRLDupKwABN5T3P8HdKSmc0VSx6_qTcw=="
org = "fit"
client = InfluxDBClient(url="http://localhost:8086", token=token, timeout=60000)
bucket = "accidents"
query_api = QueryApi(client)

buckets_api = BucketsApi(client)
bucket_name = "accidents"
buckets_api.create_bucket(bucket_name=bucket_name, org=org, retention_rules=[], description="Car_accidents")

points = []
for index, row in df_grouped.iterrows():
    point = Point("car_crashes") \
        .field("usmrceno_os", row['usmrceno_os']) \
        .field("tezce_zran_os", row['tezce_zran_os']) \
        .field("lehce_zran_os", row['lehce_zran_os']) \
        .field("hmotna_skoda", row['hmotna_skoda']) \
    .time(row['datum'], WritePrecision.NS)

    points.append(point)

batch_size = 500

write_api = client.write_api(write_options=SYNCHRONOUS)
for i in range(0, len(points), batch_size):
    batch_points = points[i:i+batch_size]
    write_api.write(bucket=bucket, org=org, record=batch_points)

client.close()
