import pymongo as pm
import geojson
from datetime import datetime

count1 = 0
count2 = 0

class Personality:
    def __init__(self, ogcfid, title, description, url_1, create_date, last_date,
                 numeric_1, date_1, date_2, list_1, location):
        global count1, count2
        self.ogcfid = ogcfid
        self.title = title
        self.description = description
        self.url_1 = url_1
        self.create_date = create_date
        self.last_date = last_date
        self.numeric_1 = numeric_1
        self.list_1 = list_1
        self.location = location
        if date_1 is not None:
            self.date_1 = datetime.fromisoformat(date_1)
        else:
            print ('1', self.title)
            count1 += 1
            self.date_1 = None

        if date_2 is not None:
            self.date_2 = datetime.fromisoformat(date_2)
        else:
            print ('2', self.title)
            count2 += 1
            self.date_2 = None
    
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
            "location": self.location
        }

personalities = []

with open("./datasets/mongo_vyznamne_osobnosti.geojson", "r") as f:
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

print('count1', count1)
print('count2', count2)


# result = client.upa.vyznamne_osobnosti.insert_many([p.dict() for p in personalities])
# print(result.inserted_ids)
# client.upa.vyznamne_osobnosti.create_index([("location", pm.GEOSPHERE)])

for i in personalities:
    if (i.url_1 is None):
        print(i.title)



# { location: { $nearSphere: { $geometry: { type: "Point", coordinates: [ 16.594622, 49.165244 ] }, $maxDistance: 50 } } }