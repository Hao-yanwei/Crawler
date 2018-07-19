# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhaopingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_name = scrapy.Field()#工作名称
    job_link = scrapy.Field()#工作链接
    job_info = scrapy.Field()#工作信息
    company = scrapy.Field()#公司
    address = scrapy.Field()#地址
    salary = scrapy.Field()#薪资
    # company_info = scrapy.Field()#公司信息

    #增加爬虫的名称和时间戳
    crawled = scrapy.Field()
    spider = scrapy.Field()

