from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from settings import read_config
import os

# load env variable file
load_dotenv(find_dotenv())
config = read_config('MONGODB')

COLLECTION_NEWS = config['COLLECTION_NEWS']
COLLECTION_NODES = config['COLLECTION_NODES']
COLLECTION_RELATIONS = config['COLLECTION_RELATIONS']
COLLECTION_COORDINATES = config['COLLECTION_COORDINATES']
DB_RAW_NAME = config['DB_RAW_NAME']
DB_RENDERED_NAME = config['DB_RENDERED_NAME']

client = MongoClient(os.environ.get('MONGODB_URL'))


def find_all(database, collection):
    '''
    Get all documents for a specific collection

    :param str collection: Collection name
    :return: List of documents
    '''
    cursor = client[database][collection].find({}, {'_id': 0})

    return list(cursor)


def find_many(database, collection, condition, projection):
    '''
    Find multiple documents

    :param str collection: Collection name
    :param dict condition: Match condition
    :return: List of documents that match condition
    '''
    cursor = client[database][collection].find(condition, projection)

    return list(cursor)