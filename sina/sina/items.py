# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class SinaItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'users'

    id = Field()
    name = Field()  # 名称
    avatar = Field()  # 图片
    cover = Field()  # 封面
    gender = Field()  # 性别
    description = Field()  # 简介
    fans_count = Field()  # 粉丝数量
    follows_count = Field()  # 关注人数
    weibos_count = Field()  # 微博数
    verified = Field()  #
    verified_reason = Field()
    verified_type = Field()
    follows = Field()  # 关注
    fans = Field()
    crawled_at = Field()


class UserRelationItem(Item):
    collection = 'users'

    id = Field()
    follows = Field()  # 关注
    fans = Field()  # 粉丝


class WeiboItem(Item):
    collection = 'weibos'

    id = Field()
    attitudes_count = Field()
    comments_count = Field()  # 评论数量
    reposts_count = Field()  #
    picture = Field()  # 图片
    pictures = Field() #
    source = Field()
    text = Field()
    raw_text = Field()
    thumbnail = Field()
    user = Field()
    created_at = Field()
    crawled_at = Field()
