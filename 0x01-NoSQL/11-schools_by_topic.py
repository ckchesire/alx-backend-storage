#!/usr/bin/env python3
"""Module to list schools with a specific topic.
"""


def schools_by_topic(mongo_collection, topic):
    """
    Returns a list of school documents having a specific topics.

    Args:
        mongo_collection: pymongo collection object
        topic (string): topic searched

    Returns:
        List of schools having the specified topic
    """
    return list(mongo_collection.find({"topics": topic}))
