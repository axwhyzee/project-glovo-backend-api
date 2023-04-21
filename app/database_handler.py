from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
import os

# load env variable file
load_dotenv(find_dotenv())

PASSWORD = os.environ.get("MONGODB_PWD")
CONNECTION_STRING = f'mongodb+srv://admin:{PASSWORD}@cluster0.xo29eao.mongodb.net/?retryWrites=true&w=majority'
DB_NAME = 'project-glovo'
COLLECTION_NEWS = 'news'
COLLECTION_NODES = 'nodes'
COLLECTION_RELATIONS = 'relations'

client = MongoClient(CONNECTION_STRING)
db = client[DB_NAME]


def find_all(collection) ->:
    '''
    Get all documents for a specific collection

    :param str collection: Collection name
    :return: List of documents
    '''
    cursor = db[collection].find({}, {'_id': 0})

    return list(cursor)


def find_many(collection, condition):
    '''
    Find multiple documents

    :param str collection: Collection name
    :param dict condition: Match condition
    :return: List of documents that match condition
    '''
    return db[collection].find(condition, {'_id': 0})