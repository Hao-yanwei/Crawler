# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JingdongspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = scrapy.Field()  # 商品链接
    project_id = scrapy.Field()  # 商品ID
    name = scrapy.Field()  # 商品名字
    comment_num = scrapy.Field()  # 评论人数
    shop_name = scrapy.Field()  # 店家名字
    price = scrapy.Field()  # 价钱
    GoodCountStr = scrapy.Field()  # 好评
    AfterCount = scrapy.Field()  # 中评
    PoorCount = scrapy.Field()  # 差评


class commentItem(scrapy.Item):
    user_name = scrapy.Field()   # 评论用户的名字
    user_id = scrapy.Field()  # 评论用户的ID
    userProvince = scrapy.Field()  # 评论用户来自的地区
    content = scrapy.Field()  # 评论内容
    good_id = scrapy.Field()  # 评论的商品ID
    good_name = scrapy.Field()  # 评论的商品名字
    date = scrapy.Field()   # 评论时间
    replyCount = scrapy.Field()   # 回复数
    score = scrapy.Field()  # 评分
    status = scrapy.Field()  # 状态
    userLevelId = scrapy.Field()  # 用户等级
    productColor = scrapy.Field()  # 商品颜色
    productSize = scrapy.Field()  # 商品大小
    userLevelName = scrapy.Field()   # 银牌会员，钻石会员等
    userClientShow = scrapy.Field()   # 来自什么 比如来自京东客户端
    isMobile = scrapy.Field()  # 是否来自手机
    days = scrapy.Field()  # 天数
    # commentTags = scrapy.Field()   # 标签