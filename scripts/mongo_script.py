import pymongo as pm
import geojson
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup

personalities = []

class Personality:
    def __init__(self, ogcfid, title, description, url_1, create_date, last_date,
                 numeric_1, date_1, date_2, list_1, location):
        global count1, count2
        self.ogcfid = ogcfid
        self.title = title
        self.description = description
        self.url_1 = url_1
        if create_date is not None:
            self.create_date = datetime.fromisoformat(create_date)
        else:
            self.create_date = None
        if last_date is not None:
            self.last_date = datetime.fromisoformat(last_date)
        else:
            self.last_date = None
        self.numeric_1 = numeric_1
        self.list_1 = list_1
        self.location = location
        if date_1 is not None:
            self.date_1 = datetime.fromisoformat(date_1)
        else:
            self.date_1 = None

        if date_2 is not None:
            self.date_2 = datetime.fromisoformat(date_2)
        else:
            self.date_2 = None
        self.education = self.get_education_external()
        

    def get_education_external(self):
        if self.url_1 is None:
            ''
        html = urlopen(self.url_1).read().decode('utf-8')
        soup = BeautifulSoup(html, "html.parser")

        content = soup.find('div', class_='content')
        rows = content.find_all('div', class_='row')

        for row in rows:
            title = row.find('span', class_='attr-title')
            if title is not None:
                if 'vzdělání' in title:

                    txt = row.find('p', class_='full')
                    if txt is not None:
                        return txt.get_text().split('\r\n')
    
    def dict(self):
        return {
            "_id": self.ogcfid,
            "title": self.title,
            "description": self.description,
            "url_1": self.url_1,
            "create_date": self.create_date,
            "last_date": self.last_date,
            "numeric_1": self.numeric_1,
            "date_1": self.date_1,
            "date_2": self.date_2,
            "list_1": self.list_1,
            "location": self.location,
            "education": self.education
        }

def load_dataset():
    global personalities
    with open("./mongo_vyznamne_osobnosti.geojson", "r") as f:
        geojson_data = geojson.load(f)
        for personality in geojson_data["features"]:
            p, g = personality["properties"], personality["geometry"]
            personalities.append(Personality(
                p["ogcfid"],
                p["title"],
                p["description"],
                p["url_1"],
                p["create_date"],
                p["last_date"],
                p["numeric_1"],
                p["date_1"],
                p["date_2"],
                p["list_1"],
                geojson.Point(g["coordinates"])
            ))

client = pm.MongoClient("mongodb://root:root@localhost:27017/?authMechanism=DEFAULT")
db = client["upa"]
col = db["vyznamne_osobnosti"]

def delete_colletion():
    client.upa.vyznamne_osobnosti.drop()

def insert_all_and_index():
    global client, personalities
    client.upa.vyznamne_osobnosti.insert_many([p.dict() for p in personalities])
    client.upa.vyznamne_osobnosti.create_index([("location", pm.GEOSPHERE)])

def query():
    start_date = datetime(1940, 1, 1)
    end_date = datetime(1940, 12, 31)
    location_point = [16.591516, 49.172261]
    max_distance = 1000

    results = col.find({
        'date_1': {'$gte': start_date, '$lte': end_date},
        'location': {
            '$near': {
                '$geometry': {
                    'type': "Point",
                    'coordinates': location_point
                },
                '$maxDistance': max_distance,
            }
        }
    }, {
    'title': 1,
    'date_1': 1
    })

    for document in results:
        print(document)
        print()

def update():
    client.upa.vyznamne_osobnosti.update_one({"_id":8388},{"$set":{"numeric_1":42}})

load_dataset()
delete_colletion()
insert_all_and_index()
query()
update()