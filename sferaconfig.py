from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.sfera

def getConfig(key):
    result = db.config.find_one({"key": key})
    return result["value"]

def addDefaultConfig():
    default = [
        {
            "key": "technician_broadcast_time",
            "value": 10
        }
    ]
    for doc in default:
        db.config.update_one({"key": doc["key"]}, {"$set": doc}, upsert=True)
