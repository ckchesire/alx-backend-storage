#!/usr/bin/env python3
"""Module that changes all topics of a school document based on name.
"""


def update_topics(mongo_collection, name, topics):
    """
    Update all topics fields of a school documents matching the name.

    Args:
        mongo_collection: pymongo collection object
        name (string): name of the school to update
        topics (list of stings): list of topics to set in the document

    Returns:
        None
    """
    mongo_collection.update_many(
            {"name": name},
            {"$set": {"topics": topics}}
    )
