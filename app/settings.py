import os

import configparser
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
    
parser = configparser.ConfigParser()
parser.read('config.ini')
config = parser['MONGODB']

COLLECTION_NEWS = config['COLLECTION_NEWS']

COLLECTION_NODES = config['COLLECTION_NODES']

COLLECTION_RELATIONS = config['COLLECTION_RELATIONS']

COLLECTION_COORDINATES = config['COLLECTION_COORDINATES']

DB_RAW_NAME = config['DB_RAW_NAME']

DB_RENDERED_NAME = config['DB_RENDERED_NAME']
    
HEADERS = {'Cache-Control': 'public, max-age=900'} # 15 min cache

MONGODB_URL = os.environ.get('MONGODB_URL')

REDIS_HOST, REDIS_PORT = os.environ.get('REDIS_URL').split(':')

REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')