from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
import uvicorn
import json
from database_handler import *


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/')
def read_root():
    return 'Index'

@app.get('/edges/')
async def get_edges():
    docs = find_all(COLLECTION_RELATIONS)

    return docs

@app.get('/nodes/')
async def get_nodes():
    docs = find_all(COLLECTION_NODES)

    return docs
    
@app.get('/news/')
async def get_news_by_key(key: str = '', page: int = 1, size: int = 10):
    docs = find_many(COLLECTION_NEWS, {'keys': {'$in': [key]}}) if key else find_all(COLLECTION_NEWS)
    size = max(1, size) # size >= 1
    pages = 1 + len(docs) // size
    page = min(max(1, page), pages) # 1 <= page <= pages

    return {
        'articles': docs[(page - 1) * size : page * size], 
        'page':     page, 
        'pages':    pages,
        'status':   'Success'
    }


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=10000, reload=True)
