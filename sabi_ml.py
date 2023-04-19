import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def getSimilar(_id, allRestaurants):

    df = pd.DataFrame(list(allRestaurants))
    df['cuisines'] = [','.join(map(str, l)).lower().replace(
        ' ', '').replace(',', ' ') for l in df['cuisines']]

    df_percent = df.sample(frac=1)

    df_percent.set_index('_id', inplace=True)
    indices = pd.Series(df_percent.index)

    tfidf = TfidfVectorizer(analyzer='word', ngram_range=(
        1, 2), min_df=0, stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df_percent['cuisines'])

    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

    # Create a list to put top restaurants
    similar_restaurants = []

    # Find the index of the hotel entered
    idx = indices[indices == _id].index[0]

    # Find the restaurants with a similar cosine-sim value and order them from bigges number
    score_series = pd.Series(
        cosine_similarities[idx]).sort_values(ascending=False)

    # Extract top 30 restaurant indexes with a similar cosine-sim value
    top30_indexes = list(score_series.iloc[0:31].index)

    # Names of the top 30 restaurants
    for each in top30_indexes:
        similar_restaurants.append(list(df_percent.index)[each])

    return similar_restaurants[:5]
