# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NovelItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #小说名称
    bookname = scrapy.Field()
    # 小说链接
    novel_url = scrapy.Field()
    #小说封面链接
    cover_url = scrapy.Field()
    #原作者
    author = scrapy.Field()
    # 原著状态
    status = scrapy.Field()
    #标签/类别
    laber = scrapy.Field()
    #简介
    description = scrapy.Field()