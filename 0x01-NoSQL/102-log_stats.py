#!/usr/bin/env python3
""" MOdel to count methods in enginx logs """
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nlogs = client.logs.nginx
    print(nlogs.count_documents({}), "logs")
    print("Methods:")
    print(f"\tmethod GET: {nlogs.count_documents({'method': 'GET'})}")
    print(f"\tmethod POST: {nlogs.count_documents({'method': 'POST'})}")
    print(f"\tmethod PUT: {nlogs.count_documents({'method': 'PUT'})}")
    print(f"\tmethod PATCH: {nlogs.count_documents({'method': 'PATCH'})}")
    print(f"\tmethod DELETE: {nlogs.count_documents({'method': 'DELETE'})}")
    print(nlogs.count_documents({"path": "/status"}), "status check")
    top_ips = nlogs.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    print("IPs:")
    for ip_data in top_ips:
        ip = ip_data["_id"]
        count = ip_data["count"]
        print(f"\t{ip}: {count}")
