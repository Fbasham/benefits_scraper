from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from search import search

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

@app.get('/{query}')
def root(query):
    results = search(query)
    return {'result': results}