# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Music163Item(scrapy.Item):
    table_name = 'music'
    id = scrapy.Field() #id
    artist = scrapy.Field() # 艺术家
    album = scrapy.Field() #专辑
    music = scrapy.Field()  # 音乐名称
    Lyric = scrapy.Field() # 歌词

class MusicComments(scrapy.Item):
    table_name = 'comments'
    id = scrapy.Field()  # id
    song = scrapy.Field() #歌曲
    nickname = scrapy.Field() #用户
    avatarurl = scrapy.Field() #头像
    comments = scrapy.Field() #评论
    hotcomment_like = scrapy.Field() #点赞

