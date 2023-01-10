import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# import nltk
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('stopwords')
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def search(query):
    df = pd.read_json('scraped.json')

    stop_words = set(stopwords.words('english'))
    stemmer = WordNetLemmatizer()
    df['text'] = df['text'].str.lower().map(lambda x: ' '.join(stemmer.lemmatize(e) for e in word_tokenize(x) if e not in stop_words))

    ss = [stemmer.lemmatize(e) for e in word_tokenize(query) if e not in stop_words]

    cv = TfidfVectorizer()
    # cv = CountVectorizer()
    count_matrix = cv.fit_transform(df['text'])
    cosine_sim = cosine_similarity(cv.transform(ss),count_matrix).mean(axis=0)
    idx = np.argsort(cosine_sim)[::-1]
    dfa = df.assign(similarity=cosine_sim)
    return {'results':dfa.loc[idx,['url','similarity']].to_dict('records')}