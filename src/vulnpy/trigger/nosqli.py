from pymongo import MongoClient
import os


def mongo_db_exists():
    client = MongoClient(serverSelectionTimeoutMS=20)
    db = client.pymongo_test

    try:
        db.posts.count_documents({})
    except Exception:  # pragma: no cover
        return False
    return True


def create_mongo_client(**kwargs):
    mongo_host = [os.environ.get("MONGODB_HOST", "localhost:27017")]
    if mongo_db_exists():
        return MongoClient(host=mongo_host, **kwargs)
    else:
        print("Pymongo service is not running.")  # pragma: no cover


client = create_mongo_client()
db = client.pymongo_test_db if client else None


def do_mongo_find(user_input):
    data = [x for x in db.spam.find({"title": user_input})]
    return data


def do_mongo_insert_one(user_input):
    return db.posts.insert_one({"title": user_input})


def do_mongo_insert_many(user_input):
    return db.posts.insert_many([{"title": user_input}])


def do_mongo_update(user_input):
    record = {"title": "Old title", "content": "PyMongo is fun!", "author": "Dani"}
    db.posts.insert_one(record)
    return db.posts.update_one(record, {"$set": {"title": user_input}})


def do_mongo_delete(user_input):
    record = {"title": "Old title", "content": "PyMongo is fun!", "author": "Dani"}
    db.posts.insert_one(record)
    return db.posts.delete_one({"title": user_input})
