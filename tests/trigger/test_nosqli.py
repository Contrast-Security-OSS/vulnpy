import pymongo
from vulnpy.trigger import nosqli
from tests.trigger.base_test import BaseTriggerTest


class TestMongoFind(BaseTriggerTest):
    @property
    def trigger_func(self):
        return nosqli.do_mongo_find

    @property
    def good_input(self):
        return (
            '{"title": "Old title", "content": "PyMongo is fun!", "author": "Dani"}',
            list,
            isinstance,
        )

    @property
    def exception_input(self):
        raise TypeError("Unsupported method")


class TestMongoInsertOne(BaseTriggerTest):
    @property
    def trigger_func(self):
        return nosqli.do_mongo_insert_one

    @property
    def good_input(self):
        return (
            '{"title": "Old title", "content": "PyMongo is fun!", "author": "Dani"}',
            pymongo.results.InsertOneResult,
            isinstance,
        )

    @property
    def exception_input(self):
        raise TypeError("Unsupported method")


class TestMongoInsertMany(BaseTriggerTest):
    @property
    def trigger_func(self):
        return nosqli.do_mongo_insert_many

    @property
    def good_input(self):
        return (
            '{"title": "Old title", "content": "PyMongo is fun!", "author": "Dani"}',
            pymongo.results.InsertManyResult,
            isinstance,
        )

    @property
    def exception_input(self):
        raise TypeError("Unsupported method")


class TestMongoUpdate(BaseTriggerTest):
    @property
    def trigger_func(self):
        return nosqli.do_mongo_update

    @property
    def good_input(self):
        return (
            '{"title": "Old title", "content": "PyMongo is fun!", "author": "Dani"}',
            pymongo.results.UpdateResult,
            isinstance,
        )

    @property
    def exception_input(self):
        raise TypeError("Unsupported method")


class TestMongoDelete(BaseTriggerTest):
    @property
    def trigger_func(self):
        return nosqli.do_mongo_delete

    @property
    def good_input(self):
        return (
            '{"title": "Old title", "content": "PyMongo is fun!", "author": "Dani"}',
            pymongo.results.DeleteResult,
            isinstance,
        )

    @property
    def exception_input(self):
        raise TypeError("Unsupported method")
