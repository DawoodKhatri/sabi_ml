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
    mongoClient = pymongo.MongoClient("mongodb+srv://abraar:am%40sabi@sabi-dev.nsxizr6.mongodb.net/")
    restaurants = mongoClient["SABI"]["restaurants"].find()

    df =  pd.DataFrame(list(restaurants))
    df['cuisines'] = [','.join(map(str, l)).lower().replace(' ','').replace(',',' ') for l in df['cuisines']]

    restaurant_names = list(df['name'])
    def get_top_words(column, top_nu_of_words, nu_of_word):
        vec = CountVectorizer(ngram_range= nu_of_word, stop_words='english')
        bag_of_words = vec.fit_transform(column)
        sum_words = bag_of_words.sum(axis=0)
        words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
        words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
        return words_freq[:top_nu_of_words]

    df_percent = df.sample(frac=1)

    df_percent.set_index('name', inplace=True)
    indices = pd.Series(df_percent.index)

    tfidf = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df_percent['cuisines'])

    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

    def recommend(name, cosine_similarities = cosine_similarities):

        # Create a list to put top restaurants
        recommend_restaurant = []

        # Find the index of the hotel entered
        idx = indices[indices == name].index[0]

        # Find the restaurants with a similar cosine-sim value and order them from bigges number
        score_series = pd.Series(cosine_similarities[idx]).sort_values(ascending=False)

        # Extract top 30 restaurant indexes with a similar cosine-sim value
        top30_indexes = list(score_series.iloc[0:31].index)

        # Names of the top 30 restaurants
        for each in top30_indexes:
            recommend_restaurant.append(list(df_percent.index)[each])
        df_new = pd.DataFrame(columns=['cuisines','rating','_id'])

        # Create the top 30 similar restaurants with some of their columns
        for each in recommend_restaurant:
            df_new = df_new.append(pd.DataFrame(df_percent[['cuisines','rating','_id']][df_percent.index == each].sample()))

        # Drop the same named restaurants and sort only the top 10 by the highest rating
        df_new = df_new.drop_duplicates(subset=['cuisines','rating','_id'], keep=False)
       # df_new = df_new.sort_values(by='rating', ascending=False).head(10)

        print('TOP %s RESTAURANTS LIKE %s WITH SIMILAR REVIEWS: ' % (str(len(df_new)), name))

        print(df_new) 
        return df_new
    recommend('Cafe Madras')

    similarRestaurants = []
    return json.loads(json_util.dumps(similarRestaurants))


app.run()
