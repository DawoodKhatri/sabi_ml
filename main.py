from flask import Flask
from pymongo import MongoClient
from bson import ObjectId, json_util
import json

app = Flask(__name__)
url = "mongodb+srv://abraar:am%40sabi@sabi-dev.nsxizr6.mongodb.net/"
mongoClient = MongoClient(url)
db = mongoClient["SABI"]


@app.route("/getSimilarRestaurants/<_id>", methods=["GET"])
def getSimilarRestaurants(_id):
    currRestaurant = db.restaurants.find_one({"_id": ObjectId(_id)})
    allRestaurants = db.restaurants.find()

    # Write your code here
    # baki mai karta hu


    similarRestaurants = []
    return json.loads(json_util.dumps(similarRestaurants))


app.run()
