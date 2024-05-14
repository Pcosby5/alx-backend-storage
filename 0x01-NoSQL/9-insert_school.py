#!/usr/bin/env python3
"""
This module provides a function to insert a document into a MongoDB collection.
"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a MongoDB collection.

    :param mongo_collection: A pymongo collection object
    :param kwargs: Key-value pairs to be added as document fields
    :return: The _id of the inserted document
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id

