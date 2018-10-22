# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class ScrapyseleniumjdPipeline(object):
    def process_item(self, item, spider):
        return item


# 存入MongoDB
class MongoPipeline(object):
    def __init__(self):
        self.MONGO_URL = 'localhost'
        self.MONGO_DB = 'test'
        self.MONGO_COLLECTION = 'JDproducts__fix'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host=self.MONGO_URL)  # 连接到MongoDB
        self.db = self.client[self.MONGO_DB]  # 指定数据库

    def process_item(self, item, spider):
        collection = self.db[self.MONGO_COLLECTION]  # 指定集合
        collection.insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()  # 关闭
