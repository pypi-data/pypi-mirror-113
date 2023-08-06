#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
from multiprocessing import Lock
import pymongo


class MongoClient():
    def __init__(self, server='127.0.0.1', port='27017', username=None, password=None, schema='env'):
        self.mongo_server = server
        self.mongo_port = port
        self.mongo_username = username
        self.mongo_password = password

        if schema == 'env':
            if os.environ.get("MONGO_URL", None) is not None:
                self.mongo_server = os.environ.get("MONGO_URL")

            if os.environ.get("MONGO_PORT", None) is not None:
                self.mongo_port = os.environ.get("MONGO_PORT")

            if os.environ.get("MONGO_USERNAME", None) is not None:
                self.mongo_username = os.environ.get("MONGO_USERNAME")

            if os.environ.get("MONGO_PASSWORD", None) is not None:
                self.mongo_password = os.environ.get("MONGO_PASSWORD")

    def set_mongo(self, server=None, port=None, username=None, password=None):
        self.mongo_server = server
        self.mongo_port = port
        self.mongo_username = username
        self.mongo_password = password
        return self

    @property
    def client(self):
        mongo_url = 'mongodb://{}:{}'.format(self.mongo_server, self.mongo_port)
        if self.mongo_username is not None and self.mongo_password is not None:
            mongo_url = 'mongodb://{}:{}@{}:{}'.format(
                self.mongo_username,
                self.mongo_password,
                self.mongo_server,
                self.mongo_port
            )
        try:
            client = pymongo.MongoClient(mongo_url)
            return client
        except Exception as err:
            raise Exception("Mongo client error!")
