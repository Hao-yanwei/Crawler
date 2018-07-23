# -*- coding: utf-8 -*-
import requests

from jingdongspider.items import commentItem
import json
import xlrd
import scrapy
from scrapy import Request


class JingdongCommentSpider(scrapy.Spider):
    name = 'comment'
    allowed_domains = ['jd.com']
    start_urls = ['https://www.jd.com']


    def parse(self, response):
        """京东"""
        url = "https://list.jd.com/list.html?cat=670,671,672&page=1&sort=sort_totalsales15_desc&trans=1&JL=6_0_0#J_main"
        yield Request(url, callback=self.parseMainPage)


    def parseMainPage(self, response):
        urls = response.xpath('//li[@class="gl-item"]/div/div[@class="p-img"]/a')
        for url in urls:
            url = url.xpath('@href').extract()
            for link in url:
                url = response.urljoin(link)
                yield Request(url, callback=self.parseDetails)


    def parseDetails(self, response):
        id= response.xpath('//a[@class="compare J-compare J_contrast"]/@data-sku').extract()[0] # 商品id

        """
        解析京东商品评论的url
        """
        com_url = 'https://sclub.jd.com/comment/productPageComments.action?productId=' + str(id) +'&score=0&sortType=5&page=0&pageSize=10'
        yield scrapy.Request(com_url, callback=self.parse_getCommentnum)

        """
        通过递归原理解析下一页
        下一页网页xpath解析地址
        """
        # comment_num = "https://club.jd.com/comment/productCommentSummaries.action?referenceIds=" + str(id)
        # com = requests.get(comment_num).text
        # date = json.loads(com)
        # comment_nums = date['CommentsCount'][0]['ShowCount']
        # comment_total = int(comment_nums)
        # if comment_total % 10 == 0:  # 算出评论的页数，一页10条评论
        #     page = comment_total//10
        # else:
        #     page = comment_total//10 + 1
        # for k in range(0, page):
        #     '''
        #     京东下一页评论接口
        #     '''
        #     url ='https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv2394&productId='+ str(id) +'&score=0&sortType=5&page='+str(k)+'&pageSize=10&isShadowSku=0&fold=1'
        #     # print(">>>>>>>>>>", url)
        #     yield scrapy.Request(url, callback=self.parseDetails)

    def parse_getCommentnum(self, response):
        js = json.loads(response.text)
        comments = js['comments']  # 该页所有评论

        items = []
        for comment in comments:
            item1 = commentItem()
            item1['user_name'] = comment['nickname']  # 用户名
            item1['user_ID'] = comment['id']       #  用户
            item1['userProvince'] = comment['userProvince']  # 用户评论用户来自的地区
            item1['content'] = comment['content']  #  评论
            item1['good_ID'] = comment['referenceId']  # 评论的商品ID
            item1['good_name'] = comment['referenceName']  # 评论的商品名字
            item1['date'] = comment['referenceTime']   # 评论时间
            item1['replyCount'] = comment['replyCount']  # 回复数
            item1['score'] = comment['score']  # 评分
            item1['status'] = comment['status']   # 状态
            item1['userLevelId'] = comment['userLevelId']  # 用户等级
            item1['productColor'] = comment['productColor']  # 商品颜色
            item1['productSize'] = comment['productSize']   # 商品大小
            item1['userLevelName'] = comment['userLevelName']  # 银牌会员，钻石会员等
            item1['isMobile'] = comment['isMobile']   # 是否来自手机
            item1['userClientShow'] = comment['userClientShow']  # 是否来自手机
            item1['days'] = comment['days']  # 天数
            items.append(item1)
        return items
