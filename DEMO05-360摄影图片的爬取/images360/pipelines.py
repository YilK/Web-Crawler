# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class Images360Pipeline(object):
    def process_item(self, item, spider):
        return item


# 将数据保存到MySQL中
class MysqlPipeline():
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):  # 类方法，参数是crawler，通过此对象我们可以拿到Scrapy的所有核心组件
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT')
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(host=self.host, user=self.user, password=self.password, port=self.port,
                                  db=self.database, charset='utf8')
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        data = dict(item)  # item是一个类字典的类型，将其转化为字典类型、
        keys = ','.join(data.keys())
        values = ','.join(['%s'] * len(data))
        sql = 'insert into image360({}) values({})'.format(keys, values)
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()
        return item


