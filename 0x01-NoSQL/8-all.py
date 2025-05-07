#!/usr/bin/env python3
"""Module that lists all documents in a MongoDN collection.
"""


def list_all(mongo_collection):
    """
    Lists all documents in a given collection

    Args:
        mongo_collection: pymongo collection object

    Returns:
        A list of all documents in the collection, or an empty list if none
    """
    if mongo_collection is None:
        return []
    return list(mongo_collection.find())
