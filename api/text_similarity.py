from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize

def text_similarity(df, query, stemmer, stop_words):
    query_vector = [stemmer.lemmatize(e) for e in word_tokenize(query) if e not in stop_words]

    vec = TfidfVectorizer()
    freq_matrix = vec.fit_transform(df['text'])
    cosine_sim = cosine_similarity(vec.transform(query_vector), freq_matrix).mean(axis=0)
    df = df.assign(similarity=cosine_sim)
    return {
        'results': df[['title','url','similarity']]
                      .query('similarity > 0')
                      .sort_values(by='similarity', ascending=False)
                      .to_dict('records')
    }