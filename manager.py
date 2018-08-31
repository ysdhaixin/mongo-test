#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pluggy
from pymongo import MongoClient
from multimedia.hookspec import DataSourceSpec, Plugin
from bson.objectid import ObjectId
from gridfs import *


class DataManager:

    def __init__(self, hook, ip='localhost', port=27020, db='video', collection='fs', path='./introduce.mp4'):
        self.hook = hook
        self.ip = ip
        self.port = port
        self.path = path
        self._db = db
        self._collection = collection
        self.obj_id = None
        self.client, self.db, self.collection = None, None, None

    def __enter__(self):
        self.client = MongoClient(self.ip, self.port)
        self.db = self.client[self._db]
        self.collection = GridFS(self.db, self._collection)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()

    def write_to_db(self):
        items = self.hook.load_source(path=self.path)
        for item in items:
            for value in item:
                with open(value, 'rb') as obj:
                    data = obj.read()
                    self.obj_id = self.collection.put(data, filename='first')
                    print(self.obj_id)

    def read_from_db(self):
        file = self.collection.get_version('first', 0)
        data = file.read()
        with open('./introduce1.mp4', 'wb') as out:
            out.write(data)

    def del_file(self, obj_id=None):
        obj_id = obj_id or self.obj_id
        self.collection.delete(ObjectId(obj_id))

    def list_name(self):
        print(self.collection.list())


def main():
    pm = pluggy.PluginManager("data-mgr")
    pm.add_hookspecs(DataSourceSpec)
    pm.register(Plugin())
    with DataManager(hook=pm.hook) as dm:
        dm.write_to_db()
        dm.read_from_db()
        dm.list_name()
        dm.del_file()


if __name__ == '__main__':
    main()

