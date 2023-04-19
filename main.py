from flask import Flask
from pymongo import MongoClient
from bson import ObjectId, json_util
import json
import os
from dotenv import load_dotenv
from sabi_ml import getSimilar

load_dotenv()
app = Flask(__name__)
mongoClient = MongoClient(os.getenv("MONGO_URI"))
db = mongoClient["SABI"]


@app.route("/getSimilarRestaurants/<_id>", methods=["GET"])
def getSimilarRestaurants(_id):
    allRestaurants = db.restaurants.find()

    similarRestaurants = db.restaurants.find(
        {"_id": {"$in": getSimilar(ObjectId(_id), allRestaurants)}})

    return json.loads(json_util.dumps(similarRestaurants))
