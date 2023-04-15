import asyncio
import bson
from bot.database.database import connect_to_database

async def load_static_collection():
    with open('sample_collection.bson', 'rb') as file:
        data = bson.decode_all(file.read())
    collection = await connect_to_database()
    await collection.insert_many(data)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(load_static_collection())
