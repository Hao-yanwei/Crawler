# -*- coding: utf-8 -*-

# Scrapy settings for zhaoping project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'zhaoping'

SPIDER_MODULES = ['zhaoping.spiders']
NEWSPIDER_MODULE = 'zhaoping.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'zhaoping (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3#下载延迟
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'zhaoping.middlewares.ZhaopingSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'zhaoping.middlewares.ZhaopingDownloaderMiddleware': 543,

    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware':None,
    # 'zhaoping.middlewares.ProxyMiddleWare':125,
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware':None


}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'zhaoping.pipelines.ZhaopingPipeline': 300,
    'zhaoping.pipelines.ExamplePipeline': 300,
    # 下面这个管道是必须要启用的--支持数据存储到redis数据库里
    'scrapy_redis.pipelines.RedisPipeline': 400,

}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

"""
scrapy-redis设置方法
"""

#按照sorted 排序顺序出队列，建议使用某一个，这样才能在redis数据库中看到,其实可以不写不影响结果
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"

#使用scrapy-redis自己调度器,不使用scrapy默认的调度器,负责去重
SCHEDULER ="scrapy_redis.scheduler.Scheduler"

#使用scrapy-redis自己的组件去重,不使用scrapy默认的去重
DUPEFILTER_CLASS ="scrapy_redis.dupefilter.RFPDupeFilter"

#调度状态持久化，不清理redis缓存，允许暂停/启动爬虫
SCHEDULER_PERSIST =True

#redis
REDIS_HOST ='192.168.0.101'

REDIS_PORT =6379

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) ' \
             'AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'

HTTPERROR_ALLOWED_CODES = [403]