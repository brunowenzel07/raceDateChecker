# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class RecingPipeline(object):
#     def process_item(self, item, spider):
#         return item
#

import pymongo
import json
import os

from scrapy.exceptions import DropItem

def isNullRecord(item):
    return not item['racecourse']


class MongoPipeline(object):

    collection_name = 'races'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    # create race if not null else drop

    def isNullRecord(item):
        return not item.racecourse

    def process_item(self, item, spider):
        if isNullRecord(item):
            raise DropItem("Not a race date %s" % item)
        dup_check = self.db[self.collection_name].find({'racedate':item['racedate']}).count()
        if dup_check == 0:
            item['noraces'] = int(item['noraces'])
            self.db[self.collection_name].insert(dict(item))
        else:
            raise DropItem("Already seen this race date %s" % item)
        # self.db[self.collection_name].insert(dict(item))
        return item




class JsonWriterPipeline(object):

    def open_spider(self, spider):
        file_for_items = os.path.isfile('items.json')

        if file_for_items:
            with open("items.json", 'r') as file:
                self.data = json.load(file)

        else:
            with open("items.json", 'a') as file:
                self.data = []
                json.dump(self.data, file)

    def close_spider(self, spider):
        with open("items.json", 'w') as file:
            json.dump(self.data, file)

    # null record {'noraces': None, 'racecourse': None, 'racedate': '20170102'}


    def process_item(self, item, spider):
        if isNullRecord(item):
            raise DropItem("Not a race date %s" % item)
        self.data.append(dict(item))
        return item

# import pymongo
#
# class MongoPipeline(object):
#
#     collection_name = 'posts'
#
#     def __init__(self, mongo_uri, mongo_db):
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             mongo_uri=crawler.settings.get('MONGO_URI'),
#             mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
#         )
#
#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]
#
#     def close_spider(self, spider):
#         self.client.close()
#
#     def process_item(self, item, spider):
#         self.db[self.collection_name].insert(dict(item))
#         return item
