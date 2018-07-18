# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import pymongo
from scrapy.conf import settings
from .items import Music163Item
import csv


class Music163Pipeline(object):
    def process_item(self, item, spider):
        return item


# class MongoPipeline(object):
#
#     def __init__(self, mongo_uri, mongo_db):
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             mongo_uri=crawler.settings.get('MONGO_URI'),
#             mongo_db=crawler.settings.get('MONGO_DB')
#         )
#
#     # 爬虫启动将会自动执行下面的方法
#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]
#
#     # 爬虫项目关闭调用的方法
#     def close_spider(self, spider):
#         self.client.close()
#
#     def process_item(self, item, spider):
#
#         self.db[item.table_name].update({'id': item.get('id')}, {'$set': dict(item)}, True)
#         return item

class WangyinPipeline(object):
    def __init__(self):
        self.f = open("wangyiyun.csv", "w")
        self.writer = csv.writer(self.f)
        self.writer.writerow(['id', 'artist', 'album', 'music', 'Lyric'])

    def process_item(self, item, spider):
        wangyiyun_list = [item['id'], item['artist'], item['album'], item['music'], item['Lyric']]

        self.writer.writerow(wangyiyun_list)
        return item

    def close_spider(self, spider):  # 关闭
        self.writer.close()
        self.f.close()


class WangyinPipeline_a(object):
    def __init__(self):
        self.f = open("wangyiyun.csv", "w")
        self.writer = csv.writer(self.f)
        self.writer.writerow(['id', 'song', 'nickname', 'avatarurl', 'hotcomment_like', 'comments'])

    def process_item(self, item, spider):
        wangyiyun_list = [item['id'], item['song'], item['nickname'], item['avatarurl'], item['hotcomment_like'],
                          item['comments']]

        self.writer.writerow(wangyiyun_list)
        return item

    def close_spider(self, spider):  # 关闭
        self.writer.close()
        self.f.close()
