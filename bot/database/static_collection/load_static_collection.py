import asyncio
import bson
from bot.database.database import connect_to_database
import os

dir_path = os.path.dirname(os.path.realpath(__file__))


async def load_static_collection():
    with open(os.path.join(dir_path, 'sample_collection.bson'), 'rb') as file:
        data = bson.decode_all(file.read())
    collection = await connect_to_database()
    await collection.insert_many(data)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(load_static_collection())
