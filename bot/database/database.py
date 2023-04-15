import os

import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv()


async def connect_to_database():
    client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("LOCAL_DATABASE"))
    db = client["aggregation"]
    sample_collection = db["sample_collection"]
    return sample_collection
