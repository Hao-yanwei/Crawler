# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import ZhaopingItem
import redis
from scrapy_redis.spiders import RedisCrawlSpider


# class ZhaopinSpider(scrapy.Spider):
class ZhaopinSpider(RedisCrawlSpider):
    name = 'zhaopin'
    redis_key = 'ZhaopinSpider:start_urls'

    allowed_domains = ['zhilian.com']
    start_urls = ['http://zhilian.com/']

    def start_requests(self):
        """智联招聘"""
        url = "https://sou.zhaopin.com/jobs/searchresult.ashx?jl=北京&kw=python"
        yield Request(url, callback=self.parseMainPage)


    def parseMainPage(self,response):
        item = ZhaopingItem()
        #获取网页中职位的url数据

        urls = response.xpath('//td[@class="zwmc"]/div/a')
        # print(urls)
        for url in urls:
            url = url.xpath('@href').extract()[0]
            # print(url)
            #通过回调函数每次调取本页url信息
            yield Request(url, meta={'item': item}, callback=self.parseDetails, dont_filter=True)


        """
        下一页网页xpath解析地址
        通过递归原理解析下一页
        """
        # next_page = response.xpath('//li[@class="pagesDown-pos"]/a')

        # if self.page <= 60:
        #     url = 'https://sou.zhaopin.com/jobs/searchresult.ashx?jl=北京&kw=python&sg=b53622afd96f46c3b72e2f2ed209169a&p='
        #     self.page += 1
        #
        #     yield scrapy.Request(url + str(self.page), callback=self.parseMainPage)
        for i in range(100):
            url = 'https://sou.zhaopin.com/?jl=北京&jt=&kw=python&kt='+str(i)
            print(url)
            print(">>>>>>>>>>>>>>>")
            yield scrapy.Request(url, callback=self.parseMainPage)


    """
    公司职位详细信息提取
    """
    def parseDetails(self,response):
        item = response.meta['item']
        job_name = response.xpath('//div[@class="fixed-inner-box"]/div[1]/h1/text()').extract()#工作名称
        job_info = response.xpath('//div[@class="tab-inner-cont"]/p[2]/text()').extract()#工作信息
        salary = response.xpath('//ul[@class="terminal-ul clearfix"]/li[1]/strong/text()').extract()#工作薪资
        address = response.xpath('//div[@class="tab-inner-cont"]/h2/text()').extract()#公司地址
        company = response.xpath('//p[@class="company-name-t"]/a/text()').extract()#公司名称
        job_link = response.xpath('//p[@class="company-name-t"]/a/@href').extract()#公司网址
        # company_info = response.xpath('//p[@class="company-name-t"]/a/@href').extract()#公司介绍
        """
        由于有些解析网页标签不存在，通过抛出异常的方式，将此标签解析为空，最后将他返回出去
        """
        try:
            item['company'] = company[0]
            item['job_info'] = job_info[0]
            item['job_name'] = job_name[0]
            item['address'] = address[0]
            item['salary'] = salary[0]
            item['job_link'] = job_link[0]
        except Exception as e:
            item['company'] = "空"
            item['job_info'] = "空"
            item['job_name'] = "空"
            item['salary'] = "空"
            item['address'] = "空"
            item['job_link'] = "空"
        yield item

