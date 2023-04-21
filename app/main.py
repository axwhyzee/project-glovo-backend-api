from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn
from database_handler import *


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/')
def read_root() -> str:
    return 'Index'

@app.get('/edges/')
async def get_edges() -> list[dict]:
    docs = find_all(COLLECTION_RELATIONS)

    return docs

@app.get('/nodes/')
async def get_nodes() -> list[dict]:
    docs = find_all(COLLECTION_NODES)

    return docs

@app.get('/news/')
async def get_news() -> list[dict]:
    # _id, title, url, datetime, key1, key2, key3, key4, key5
    docs = find_all(COLLECTION_NEWS)[:10]

    print(docs)

    return docs

# to run ...
# pip install -r API_requirements.txt
# uvicorn API:app --host 0.0.0.0 --port 10000

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=10000, reload=True)