from flask import Flask
from pymongo import MongoClient
from bson import ObjectId, json_util
import json
from sabi_ml import getSimilar

app = Flask(__name__)
url = "mongodb+srv://abraar:am%40sabi@sabi-dev.nsxizr6.mongodb.net/"
mongoClient = MongoClient(url)
db = mongoClient["SABI"]


@app.route("/getSimilarRestaurants/<_id>", methods=["GET"])
def getSimilarRestaurants(_id):
    allRestaurants = db.restaurants.find()

    similarRestaurants = db.restaurants.find(
        {"_id": {"$in": getSimilar(ObjectId(_id), allRestaurants)}})

    return json.loads(json_util.dumps(similarRestaurants))


app.run()
