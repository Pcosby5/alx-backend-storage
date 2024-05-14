#!/usr/bin/env python3
"""
This module provides a function to list all documents in a MongoDB collection.
"""


def list_all(mongo_collection):
    """
    Lists all documents in a MongoDB collection.

    :param mongo_collection: A pymongo collection object
    :return: A list of all documents in the collection
    """
    documents = mongo_collection.find()
    
    # Convert cursor to list directly, no need to check count
    return list(documents)

