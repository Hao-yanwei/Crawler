# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from novel.items import NovelItem
from scrapy_redis.spiders import RedisCrawlSpider


class QidianSpider(RedisCrawlSpider):#继承scrapy-redis中定义好的类
    name = 'qidian'
    allowed_domains = ['qidian.com']
    # start_urls = ['http://qidian.com/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'novel.pipelines.NovelPipeline': 10,
        }
    }

    def start_requests(self):
        """爬取网页"""
        url = 'https://www.qidian.com/all'
        yield Request(url, callback=self.parseMainPage)

    def parseMainPage(self,response):
        urls = response.xpath('//div[@class="book-mid-info"]/h4')
        for x in urls:
            item = NovelItem()
            novel_url = x.xpath('a/@href').extract()
            all_url = response.urljoin(novel_url[0])
            item['novel_url'] = all_url  # 小说链接
            for url in novel_url:
                url = response.urljoin(url)
                yield Request(url, meta={'meta': item}, callback=self.parseDetails)


        """
        通过递归原理解析下一页
        下一页网页xpath解析地址
        """
        next_page = response.xpath('//*[@id="page-container"]/div/ul/li[last()]/a')
        for page in next_page:
            pages = page.xpath('@href').extract()[0]
            page = response.urljoin(pages)
            print(page)
            yield Request(page, callback=self.parseMainPage, dont_filter=True)

    def parseDetails(self,response):
        item = response.meta['meta']
        bookname = response.xpath("//div[@class='book-info ']/h1/em/text()").extract()  # 书名
        author = response.xpath("//a[@class='writer']/text()").extract()  # 作者
        labers = response.xpath("//p[@class='tag']/a/text()").extract()  # 标签
        laber = ",".join(labers)
        statu = response.xpath("//p[@class='tag']/span/text()").extract()  # 状态
        status = ",".join(statu)
        cover_urls = response.xpath("//a[@id='bookImg']/img/@src").extract()   # 图片链接
        cover_url = response.urljoin(cover_urls[0])
        descriptions = response.xpath("//*[@class='book-intro']/p/text()").extract()  # 描述
        description = "".join(descriptions).strip()

        item['bookname'] = bookname[0]
        if author:
            item['author'] = author[0]
        else:
            item['author'] = 'null'

        if laber:
            item['laber'] = laber
        else:
            item['laber'] = 'null'

        if status:
            item['status'] = status
        else:
            item['status'] = 'status'

        if cover_url:
            item['cover_url'] = cover_url
        else:
            item['cover_url'] = 'null'

        if description:
            item['description'] = description
        else:
            item['description'] = 'null'
        yield item

