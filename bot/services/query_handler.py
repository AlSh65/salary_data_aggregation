from datetime import datetime, timedelta
from bot.database.database import connect_to_database


def create_query(dt_from, dt_upto):
    query = {
        "dt": {
            "$gte": dt_from,
            "$lte": dt_upto
        }
    }
    return query


def create_group_field(group_type):
    if group_type == "month":
        group_field = {"$month": "$dt"}
    elif group_type == "day":
        group_field = {"$dayOfYear": "$dt"}
    elif group_type == "hour":
        group_field = {"$hour": "$dt"}
    return group_field


def aggregate_data(sample_collection, query, group_field):
    pipeline = [
        {"$match": query},
        {"$addFields": {"date": {"$dateToString": {"format": "%Y-%m-%dT%H:%M:%S.%LZ", "date": "$dt"}}}},
        {"$group": {
            '_id': group_field,
            "date": {"$first": "$date"},
            "count": {"$sum": "$value"}
        }},
        {"$sort": {"_id": 1}}
    ]

    aggregated_data = list(sample_collection.aggregate(pipeline))
    return aggregated_data


def create_labels_and_dataset(aggregated_data, group_type, dt_from, dt_upto):
    labels = []
    dataset = []

    if group_type == "month":
        while dt_from <= dt_upto:
            labels.append(dt_from.isoformat())
            count = 0
            for data in aggregated_data:
                if datetime.fromisoformat(data['date'][:-1]).month == dt_from.month and datetime.fromisoformat(
                        data['date'][:-1]).year == dt_from.year:
                    count = data["count"]
                    break
            dataset.append(count)
            if dt_from.month == 12:
                dt_from = dt_from.replace(year=dt_from.year + 1, month=1, day=1)
            else:
                dt_from = dt_from.replace(month=dt_from.month + 1, day=1)

    elif group_type == "day":
        while dt_from <= dt_upto:
            labels.append(dt_from.isoformat())
            count = 0
            for data in aggregated_data:
                if datetime.fromisoformat(data['date'][:-1]).date() == dt_from.date():
                    count = data["count"]
                    break
            dataset.append(count)
            dt_from += timedelta(days=1)

    elif group_type == "hour":
        while dt_from <= dt_upto:
            labels.append(dt_from.isoformat())
            count = 0
            for data in aggregated_data:
                if dt_from <= datetime.fromisoformat(data['date'][:-1]) < dt_from + timedelta(hours=1):
                    count = data['count']
                    break
            dataset.append(count)
            dt_from += timedelta(hours=1)

    return labels, dataset


def get_aggregated_data(user_data):
    sample_collection = connect_to_database()
    dt_from = datetime.fromisoformat(user_data["dt_from"])
    dt_upto = datetime.fromisoformat(user_data["dt_upto"])

    query = create_query(dt_from, dt_upto)
    group_field = create_group_field(user_data["group_type"])
    aggregated_data = aggregate_data(sample_collection, query, group_field)

    labels, dataset = create_labels_and_dataset(aggregated_data, user_data["group_type"], dt_from, dt_upto)

    response = {"dataset": dataset, "labels": labels}

    return response
