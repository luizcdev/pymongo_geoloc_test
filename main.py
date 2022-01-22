from flask import Flask, request, jsonify
from bson.son import SON
from pymongo import MongoClient, GEOSPHERE

app = Flask(__name__)
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client['sample_db']
db.locations.create_index([("location", GEOSPHERE)])


@app.route('/create', methods=['POST'])
def create():
    request_data = request.get_json()
    print((request_data))
    document = {
        "id": request_data["id"],
        "text": request_data["text"],
        "user": request_data["user"],
        "location": {
            "type": "Point",
            "coordinates": [float(request_data["latitude"]), float(request_data["longitude"])]
        }

    }
    persisted_document = db.locations.insert_one(document)
    print(persisted_document.inserted_id)
    return jsonify({"document_id": str(persisted_document.inserted_id)})

@app.route('/near/<latitude>/<longitude>/<maxDistance>')
def near(latitude, longitude, maxDistance):
    query = {"location": SON([("$nearSphere", [float(latitude), float(longitude)]), ("$maxDistance", float(maxDistance))])}
    result = db.locations.find(query).limit(3)
    print(result.explain)
    print("result: " + str(result))
    for doc in result:
        print(doc)

    return jsonify({"ok": "ok"})



app.run(debug=True, port=5000)
