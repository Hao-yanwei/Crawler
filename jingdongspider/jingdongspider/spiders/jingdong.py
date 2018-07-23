# -*- coding: utf-8 -*-
import requests
from jingdongspider.items import JingdongspiderItem
import scrapy
import re
import json
from scrapy import Request


class JingdongSpider(scrapy.Spider):
    name = 'jingdong'
    allowed_domains = ['jd.com']
    start_urls = ['https://www.jd.com']


    def parse(self, response):
        """京东"""
        url = "https://list.jd.com/list.html?cat=670,671,672&page=1&sort=sort_totalsales15_desc&trans=1&JL=6_0_0#J_main"
        yield Request(url, callback=self.parseMainPage)


    def parseMainPage(self, response):
        urls = response.xpath('//li[@class="gl-item"]/div/div[@class="p-img"]/a')
        for url in urls:
            item = JingdongspiderItem()
            url = url.xpath('@href').extract()
            all_url = response.urljoin(url[0])
            item['link'] = all_url  # 商品链接
            for link in url:
                url = response.urljoin(link)
                yield Request(url, meta={'meta': item}, callback=self.parseDetails)



        """
        通过递归原理解析下一页
        下一页网页xpath解析地址
        """
        next_page = response.xpath('//a[@class="pn-next"]')
        for page in next_page:
            pages = page.xpath('@href').extract()[0]
            page = response.urljoin(pages)
            print(">>>>>>>>>>>>>", page)
            yield Request(page, callback=self.parseMainPage, dont_filter=True)


    def parseDetails(self, response):
        item = response.meta['meta']
        id= response.xpath('//a[@class="compare J-compare J_contrast"]/@data-sku').extract()[0] # 商品id
        item['project_id'] = id
        shop_name = response.xpath('//div[@class="name"]/a/text()').extract()[0] # 商店名称
        print(">>>>>>",shop_name)
        item['shop_name'] = shop_name
        item['name'] = response.xpath('//div[@class="sku-name"]/text()').extract()[0].strip() # 名称
        """
        获取京东商品价格的url
        """
        price_url = "https://p.3.cn/prices/mgets?callback=jQuery8876824&skuIds=" + str(id)
        price = requests.get(price_url).text
        money = re.findall(r'\"p\"\:\"(.*?)\"}]\)', price)
        item['price'] = money[0]

        """
        获取京东商品评论数量
        """
        comment_num = "https://club.jd.com/comment/productCommentSummaries.action?referenceIds=" + str(id)
        yield scrapy.Request(comment_num, meta={'item': item}, callback=self.parse_getCommentnum)
        """
        通过正则表达式解析评论人数
        """
        # comment_nums = requests.get(comment_num).text
        # nums = re.findall(r'\"ShowCountStr\"\:\"(.*?)\"', comment_nums)
        # print(">>>>>>>", nums)
        # page = urllib.urlopen(comment_num)
        # data = page.read()
        # print(data)

    def parse_getCommentnum(self, response):
        item = response.meta['item']
        # response.text是一个json格式的
        date = json.loads(response.text)
        # print(date)
        item['comment_num']= date['CommentsCount'][0]['CommentCountStr']
        item['AfterCount'] = date['CommentsCount'][0]['AfterCount']
        item['GoodCountStr']= date['CommentsCount'][0]['GoodCountStr']
        item['PoorCount']= date['CommentsCount'][0]['PoorCount']

        # for field in item.fields:
        #     try:
        #         item[field] = eval(field)
        #     except:
        #         print('Field is not defined', field)
        yield item



