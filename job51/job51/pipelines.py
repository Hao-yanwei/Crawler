# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import json
import os
"""
将爬取信息存入mysql
"""
class Job51Pipeline(object):
	def process_item(self, item, spider):
		return item

class DBPipeline(object):
	@classmethod
	def from_crawler(cls, crawler):
		return cls(host = crawler.settings.get('HOST'),\
				   user = crawler.settings.get('USER'),\
				   pwd = crawler.settings.get('PWD'),\
				   dbname = crawler.settings.get('DBNAME'),\
				   tname = crawler.settings.get('TABLE'),\
				   feeds = crawler.settings.get('MYSQLFEEDS'))

	def __init__(self, host='localhost', user='', pwd='', \
				 dbname='',tname='', feeds=[]):
		self.host = host
		self.user = user
		self.pwd = pwd
		self.db = dbname
		self.table = tname
		self.feeds = feeds
	# 打开数据库
	def open_spider(self, spider):
		self.dbcon = pymysql.connect(self.host, self.user, \
									 self.pwd, self.db, charset='utf8')
		self.cur = self.dbcon.cursor()
	# 关闭数据库
	def close_spider(self, spider):
		self.dbcon.close()

	def process_item(self, item, spider):
		info = dict(item)
		# 注入sq语句
		sql = 'insert into jobinfo(addr,jobname,pay,web_add,company,company_info) values'
		values = '(%s)' % (('%s,' * (len(self.feeds)))[:-1])
		sql += values
		rowinfo = [info.get(key, ' ') for key in self.feeds]
		print(sql, rowinfo)
		self.cur.execute(sql, rowinfo)
		self.dbcon.commit()
		return item

