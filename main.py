from flask import Flask
from pymongo import MongoClient
from bson import ObjectId, json_util
import json
import os
from dotenv import load_dotenv
from sabi_ml import getSimilar
import pymongo
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.metrics.pairwise import linear_kernel

load_dotenv()
app = Flask(__name__)
print(os.getenv("MONGO_URI"))
mongoClient = MongoClient(os.getenv("MONGO_URI"))
db = mongoClient["SABI"]


@app.route("/getSimilarRestaurants/<_id>", methods=["GET"])
def getSimilarRestaurants(_id):
    allRestaurants = db.restaurants.find()

    similarRestaurants = db.restaurants.find(
        {"_id": {"$in": getSimilar(ObjectId(_id), allRestaurants)}})

    return json.loads(json_util.dumps(similarRestaurants))
