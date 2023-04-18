import os

import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv()


async def connect_to_database():
    client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get("LOCAL_DATABASE", default='mongodb://localhost:27017/'))
    db = client["aggregation"]
    sample_collection = db["sample_collection"]
    return sample_collection
