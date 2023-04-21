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
async def get_news():
    # _id, title, url, datetime, keywords
    docs = find_all(COLLECTION_NEWS)

    return docs

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=10000, reload=True)