from pymongo import MongoClient

from settings import MONGODB_URL


client = MongoClient(MONGODB_URL)

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