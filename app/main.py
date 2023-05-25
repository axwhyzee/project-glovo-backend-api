from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import FastAPI
import uvicorn
from database_handler import (
    COLLECTION_NEWS,
    COLLECTION_NODES,
    COLLECTION_RELATIONS,
    COLLECTION_COORDINATES,
    DB_RAW_NAME,
    DB_RENDERED_NAME,
    find_all,
    find_many
)


headers = {'Cache-Control': 'public, max-age=900'} # 15 min cache

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/')
def read_root():
    return JSONResponse(content='Index', headers=headers)

@app.get('/edges/')
async def get_edges():
    docs = find_all(
        database=DB_RAW_NAME, 
        collection=COLLECTION_RELATIONS
    )

    return JSONResponse(content=docs, headers=headers)

@app.get('/nodes/')
async def get_nodes():
    docs = find_all(
        database=DB_RAW_NAME,
        collection=COLLECTION_NODES
    )

    return JSONResponse(content=docs, headers=headers)
    
@app.get('/news/')
async def get_news_by_key(key: str = '', page: int = 1, size: int = 10):
    docs = find_many(
        database=DB_RAW_NAME,
        collection=COLLECTION_NEWS, 
        condition={'keys': {'$in': [key]}}, 
        projection={'_id': 0, 'content': 0}
    ) if key else find_all(COLLECTION_NEWS)
    
    size = max(1, size) # size >= 1
    pages = 1 + len(docs) // size
    page = min(max(1, page), pages) # 1 <= page <= pages

    content = {
        'articles': docs[(page - 1) * size : page * size], 
        'page': page, 
        'pages': pages,
        'status': 'Success'
    }

    return JSONResponse(content=content, headers=headers)

@app.get('/coordinates/')
async def get_prerendered_coordinates():
    docs = find_all(
        database=DB_RENDERED_NAME, 
        collection=COLLECTION_COORDINATES
    )

    return JSONResponse(content=docs, headers=headers)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=10000, reload=True)
