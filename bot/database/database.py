import os

import pymongo
from dotenv import load_dotenv

load_dotenv()


def connect_to_database():
    client = pymongo.MongoClient(os.getenv("LOCAL_DATABASE"))
    db = client["aggregation"]
    sample_collection = db["sample_collection"]
    return sample_collection
