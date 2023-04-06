import bson
from bot.database.database import connect_to_database

with open('sample_collection.bson', 'rb') as file:
    data = bson.decode_all(file.read())
collect = connect_to_database()
collect.insert_many(data)