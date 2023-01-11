from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from search import search

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

@app.get('/{query}')
def root(query):
    results = search(query)
    return results


if __name__=='__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)