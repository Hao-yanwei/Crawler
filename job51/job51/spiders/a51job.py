# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import logging
from ..items import Job51Item
from scrapy import FormRequest

class A51jobSpider(scrapy.Spider):
    name = '51job'
    allowed_domains = ['51job.com']
    start_urls = ['http://51job.com/']

    def start_requests(self):
        """51job网址，yield生成器有秩序的执行操作"""
        url = "https://search.51job.com/list/010000,000000,0000,00,9,99,python,2,1.html?" \
              "lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&" \
              "confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
        yield Request(url, callback=self.parseMainPage)

    def parseMainPage(self,response):
        # print("333333")
        # web_adds = response.xpath('//*[@id="resultList"]/div/span[1]/a/@href').extract()
        # companys = response.xpath('//div[@class="dw_table"]/div/span/a/text()').extract()

        item = Job51Item()

        urls = response.xpath('//*[@id="resultList"]/div/p/span/a')

        for url in urls:
            url = url.xpath('@href').extract()[0]
            # item['company'] = company
            # print(url)
            # print(rmeta)
            yield Request(url, meta={'item': item}, callback=self.parseDetails)
                # break

        # 通过递归原理解析下一页
        """下一页网页xpath解析地址"""
        next_page = response.xpath('//*[@id="resultList"]/div[55]/div/div/div/ul/li[8]/a')
        for page in next_page:
            page = page.xpath('@href').extract()[0]
            print(page)
            yield Request(page,callback=self.parseMainPage)
            # break

    def parseDetails(self,response):
        item = response.meta['item']
        # print(item)
        company_info = ','.join(response.xpath('//div[@class="bmsg job_msg inbox"]/p/text()').extract())
        pay = response.xpath('//div[@class="cn"]/strong/text()').extract()
        addr = response.xpath('//div[@class="cn"]/span/text()').extract()
        jobname = response.xpath('//div[@class="cn"]/h1/text()').extract()
        company = response.xpath('//div[@class="cn"]/p/a/text()').extract()
        web_add = response.xpath('//div[@class="cn"]/p/a/@href').extract()
        company_info = company_info.strip()
        # print(company)
        """由于有些解析网页标签不存在，通过抛出异常的方式，将此标签解析为空，最后将他返回出去"""
        try:
            item['company'] = company
            item['company_info'] = company_info
            item['jobname'] = jobname[0]
            item['addr'] = addr[0]
            item['pay'] = pay[0]
            item['web_add'] = web_add[0]
        except Exception as e:
            item['company'] = "空"
            item['company_info'] = "空"
            item['jobname'] = "空"
            item['addr'] = "空"
            item['pay'] = "空"
            item['web_add'] = "空"
        return item


