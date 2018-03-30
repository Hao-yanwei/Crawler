# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Job51Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    jobname = scrapy.Field()
    addr = scrapy.Field()
    pay = scrapy.Field()
    company = scrapy.Field()
    company_info = scrapy.Field()
    web_add = scrapy.Field()
    # pass
