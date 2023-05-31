import json

from cryptography.fernet import Fernet
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import FastAPI
import redis
import uvicorn

from database_handler import (
    find_all,
    find_many
)
from settings import (
    API_KEY,
    COLLECTION_NEWS,
    COLLECTION_NODES,
    COLLECTION_RELATIONS,
    COLLECTION_COORDINATES,
    DB_RAW_NAME,
    DB_RENDERED_NAME,
    FERNET_KEY,
    HEADERS,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_PASSWORD
)


r = redis.Redis(
    host=REDIS_HOST, 
    port=int(REDIS_PORT), 
    password=REDIS_PASSWORD
)

fernet = Fernet(FERNET_KEY)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/')
def read_root() -> JSONResponse:
    return JSONResponse(content='Index', headers=HEADERS)

@app.get('/edges/')
async def get_edges() -> JSONResponse:
    cache = r.get('edges')
    if cache:
        docs = json.loads(cache)
    else:
        docs = find_all(
            database=DB_RAW_NAME, 
            collection=COLLECTION_RELATIONS
        )
        r.set('edges', json.dumps(docs))

    return JSONResponse(content=docs, headers=HEADERS)

@app.get('/nodes/')
async def get_nodes() -> JSONResponse:
    cache = r.get('nodes')
    if cache:
        docs = json.loads(cache)
    else:
        docs = find_all(
            database=DB_RAW_NAME,
            collection=COLLECTION_NODES
        )
        r.set('nodes', json.dumps(docs))

    return JSONResponse(content=docs, headers=HEADERS)
    
@app.get('/news/')
async def get_news_by_key(
    key: str = '', 
    page: int = 1, 
    size: int = 10
) -> JSONResponse:
    cache_key = f'news/?key={key}&page={page}&size={size}'
    cache = r.get(cache_key)
    if cache:
        content = json.loads(cache)
    else:
        docs = find_many(
            database=DB_RAW_NAME,
            collection=COLLECTION_NEWS, 
            condition={'keys': key}, 
            projection={'_id': 0}
        ) if key else find_all(
            database=DB_RAW_NAME,
            collection=COLLECTION_NEWS
        )
        size = max(1, size) # size >= 1
        pages = 1 + len(docs) // size
        page = min(max(1, page), pages) # 1 <= page <= pages
        content = {
            'articles': docs[(page - 1) * size : page * size], 
            'page': page, 
            'pages': pages,
            'status': 'Success'
        }
        r.set(cache_key, json.dumps(content))
    
    return JSONResponse(content=content, headers=HEADERS)

@app.get('/coordinates/')
async def get_prerendered_coordinates() -> JSONResponse:
    cache = r.get('coordinates')
    if cache:
        docs = json.loads(cache)
    else:
        docs = find_all(
            database=DB_RENDERED_NAME, 
            collection=COLLECTION_COORDINATES
        )
        r.set('coordinates', json.dumps(docs))

    return JSONResponse(content=docs, headers=HEADERS)

@app.get('/cluster/')
async def get_news_cluster(centroid: str) -> JSONResponse:
    cache_key = f'cluster/?centroid={centroid}'
    cache = r.get(cache_key)
    if not cache:
        docs = json.loads(cache)
    else:
        peripherals = find_many(
            database=DB_RAW_NAME,
            collection=COLLECTION_RELATIONS,
            condition={'$or': [{'src': centroid}, {'dst': centroid}]},
            projection={'_id':0, 'dst': 1, 'src': 1}
        )
        keys = set()
        for peripheral in peripherals:
            keys.add(peripheral['src'])
            keys.add(peripheral['dst'])
        keys.add(centroid)
        docs = find_many(
            database=DB_RAW_NAME,
            collection=COLLECTION_NEWS,
            condition={'keys': {'$in': list(keys)}}, 
            projection={'_id': 0}
        )
        r.set(cache_key, json.dumps(docs))

    return JSONResponse(content=docs, headers=HEADERS)

@app.get('/flush-cache/')
async def flush_cache(token: str) -> JSONResponse:
    if fernet.decrypt(token.encode('utf-8')).decode('utf-8') == API_KEY:
        r.flushdb()
        return JSONResponse(content={'status': 'Success'})
    return JSONResponse(content={'status': 'Invalid API key'})

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=10000, reload=True)
