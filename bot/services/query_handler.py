from datetime import datetime, timedelta
from bot.database.database import connect_to_database


async def create_group_field(group_type):
    if group_type == "month":
        group_field = {"$month": "$dt"}
    elif group_type == "day":
        group_field = {"$dayOfYear": "$dt"}
    elif group_type == "hour":
        group_field = {"$hour": "$dt"}
    return group_field

async def get_date_from_parts(group_type):
    if group_type == "month":
        date = {
            'year': '$date.year',
            'month': '$date.month'
        }
    elif group_type == "day":
        date = {
            'year': '$date.year',
            'month': '$date.month',
            'day': '$date.day',
        }
    elif group_type == "hour":
        date = {
            'year': '$date.year',
            'month': '$date.month',
            'day': '$date.day',
            'hour': '$date.hour'
        }
    return date

async def aggregate_data(sample_collection, dt_from, dt_upto, group_field, group_type, date_parts):
    pipeline = [
        {"$match": {
            "dt": {
                "$gte": dt_from,
                "$lte": dt_upto,
            },
        }},
        {"$addFields": {"date": {"$dateToParts": {"date": "$dt"}}}},
        {"$group": {
            '_id': group_field,
            "date": {"$first": "$date"},
            "count": {"$sum": "$value"}
        }},
        {"$project": {
            "_id": 0,
            "count": 1,
            "date": {
                "$dateFromParts": date_parts,
            },
        }},
        {"$densify": {
            "field": "date",
            "range": {
                "step": 1,
                "unit": group_type,
                "bounds": [dt_from, dt_upto + timedelta(seconds=1)],
            },
        },
        },
        {"$set": {
            "count": {"$ifNull": ["$count", 0]}
        }},

        {"$sort": {"date": 1}}
    ]

    aggregated_data = await sample_collection.aggregate(pipeline).to_list(None)
    return aggregated_data


async def create_labels_and_dataset(aggregated_data):
    labels = []
    dataset = []

    for data in aggregated_data:
        dataset.append(data["count"])
        labels.append(data["date"].isoformat())

    return labels, dataset


async def get_aggregated_data(user_data):
    sample_collection = await connect_to_database()
    dt_from = datetime.fromisoformat(user_data["dt_from"])
    dt_upto = datetime.fromisoformat(user_data["dt_upto"])
    group_type = user_data["group_type"]

    date_parts = await get_date_from_parts(group_type)
    group_field = await create_group_field(group_type)

    aggregated_data = await aggregate_data(sample_collection, dt_from, dt_upto, group_field, group_type, date_parts)

    labels, dataset = await create_labels_and_dataset(aggregated_data)

    response = {"dataset": dataset, "labels": labels}
    return response