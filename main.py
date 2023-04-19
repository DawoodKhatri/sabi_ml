from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId, json_util
import json
import os
from dotenv import load_dotenv
from sabi_ml import getSimilar

load_dotenv()
app = Flask(__name__)
CORS(app)
mongoClient = MongoClient(os.getenv("MONGO_URI"))
db = mongoClient["SABI"]


@app.route("/getSimilarRestaurants/<_id>", methods=["GET"])
def getSimilarRestaurants(_id):
    try:
        allRestaurants = db.restaurants.find()

        similarRestaurants = db.restaurants.find(
            {"_id": {"$in": getSimilar(ObjectId(_id), allRestaurants)}})

        similarRestaurants = json.loads(json_util.dumps(similarRestaurants))

        for restaurant in similarRestaurants: 
            restaurant["_id"] = str(restaurant["_id"]["$oid"])

        response = {"success": True, "data": similarRestaurants}

        return jsonify(response)
    except Exception as e:
        response = {"success": False, "message": str(e)}
        return jsonify(response)
