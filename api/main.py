from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

import pandas as pd
from sentence_transformers import SentenceTransformer

# import nltk
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('stopwords')
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from text_similarity import text_similarity
from semantic_similarity import semantic_similarity


# read in dataframe only once
df = pd.read_json('scraped.json')


## SEMANTIC SIMILARITY
# encodings take a long time to execute => run once
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
corpus_embeddings = model.encode(df['text'].values)


## TEXT SIMILARITY
dfc = df.copy()
stop_words = set(stopwords.words('english'))
stemmer = WordNetLemmatizer()
dfc['text'] = dfc['text'].str.lower().map(lambda x: ' '.join(stemmer.lemmatize(e) for e in word_tokenize(x) if e not in stop_words))


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

@app.get('/text-similarity/{query}')
def text_similarity_results(query):
    results = text_similarity(dfc, query, stemmer, stop_words)
    return results

@app.get('/semantic-similarity/{query}')
def semantic_similarity_results(query):
    results = semantic_similarity(df, query, model, corpus_embeddings)
    return results


if __name__=='__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)