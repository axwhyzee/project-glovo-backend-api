from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
import uvicorn
import json
from database_handler import *


NEWS_CHUNK_SIZE = 10 

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
async def get_news_by_key(request: Request):
    key = ""
    page = 1

    try:
        request_body = await request.json()
    except json.decoder.JSONDecodeError:
        print('Request body not in JSON format')

        return {
            'articles': [],
            'page':     0,
            'pages':    0,
            'status':   'Request body not in JSON format'
        }

    if 'key' in request_body:
        key = request_body['key']

    if 'page' in request_body and page > 0:
        page = request_body['page']

    docs = find_many(COLLECTION_NEWS, {'keys': {'$in': [key]}}) if key else find_all(COLLECTION_NEWS)
    pages = 1 + len(docs) // NEWS_CHUNK_SIZE

    return {
        'articles': docs[(page - 1) * NEWS_CHUNK_SIZE : page * NEWS_CHUNK_SIZE], 
        'page':     page, 
        'pages':    pages,
        'status':   'Success'
    }


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=10000)
