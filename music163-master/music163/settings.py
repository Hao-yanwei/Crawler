# -*- coding: utf-8 -*-

# Scrapy settings for music163 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'music163'

SPIDER_MODULES = ['music163.spiders']
NEWSPIDER_MODULE = 'music163.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'music163 (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider.py middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'music163.middlewares.Music163SpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'music163.middlewares.MyCustomDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html

ITEM_PIPELINES = {
    # 'music163.pipelines.Music163Pipeline': 300,
    # 'music163.pipelines.MongoPipeline': 300,
    'music163.pipelines.WangyinPipeline': 400,  # 歌曲
    # 'music163.pipelines.WangyinPipeline_a': 500, #热门评论
}

# MONGODB_HOST = '127.0.0.1'
# MONGODB_PORT = 27017
# MONGODB_DBNAME = 'music163'
# MONGODB_DOCNAME_GESHOU = 'singer'
# MONGODB_DOCNAME_MUSICS = 'musics'

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': '_ntes_nuid=3a4d89f0c9038693b333a22f4b642c68; '
              'vjuids=-1a3b24fc8.15b2ecae386.0.111c5d3d1fc22; '
              '__gads=ID=6a7aa0e876406423:T=1491138693:S=ALNI_MaExFsEzyZqzyQEKj50f8vRBn_IKw; '
              '_ntes_nnid=3a4d89f0c9038693b333a22f4b642c68,1510668204960; '
              'UM_distinctid=160df8bea064f3-0c4115b83f311e-19174638-100200-160df8bea07333; '
              'vinfo_n_f_l_n3=b3483ce3acd53e98.1.8.1498570383884.1517205080005.1517396109155;'
              'mp_MA-94A1-BB29DC5DA865_hubble=%7B%22deviceUdid%22%3A%20%22c295b809-67cc-4c38-82a6-9bcf97770d0e%22%2C'
              '%22updatedTime%22%3A%201521632517617%2C%22sessionStartTime%22%3A%201521632517617%2C%22sessionReferrer'
              '%22%3A%20%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DtWZBxV4VaurH47Pk5-MO2n9yc1LUT1sYyrvCX3-8Fkq%26wd'
              '%3D%26eqid%3Ddbac5314000622b5000000035ab23ff8%22%2C%22sessionUuid%22%3A%20%22534e1790-1308-4047-a55d'
              '-461d01af814e%22%2C%22initial_referrer%22%3A%20%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl'
              '%3DtWZBxV4VaurH47Pk5-MO2n9yc1LUT1sYyrvCX3-8Fkq%26wd%3D%26eqid%3Ddbac5314000622b5000000035ab23ff8%22%2C'
              '%22initial_referring_domain%22%3A%20%22www.baidu.com%22%2C%22persistedTime%22%3A%201521632517617%2C'
              '%22LASTEVENT%22%3A%20%7B%22eventId%22%3A%20%22da_screen%22%2C%22time%22%3A%201521632517626%7D%7D; '
              'usertrack=ezq0pVqzhKMznzDLA4TnAg==; _ga=GA1.2.24031522.1521714634; '
              'mail_psc_fingerprint=343191115c0f3f008a757b4952479fec; __e_=1526037734321; '
              'nts_mail_user=13683690736@163.com:-1:1; __f_=1526884112085; vjlast=1491138700.1527162792.11; '
              '__utma=187553192.24031522.1521714634.1527162700.1527306894.2; '
              '__utmz=187553192.1527306894.2.2.utmcsr=reg.163.com|utmccn=(referral)|utmcmd=referral|utmcct=/Main.jsp; '
              'P_INFO=m15032086039@163.com|1528366468|0|other|00&99|heb&1528366264&other#heb&130200#10#0#0|150039&1'
              '|urs|15032086039@163.com; hb_MA-BFF5-63705950A31C_source=mooc.study.163.com; '
              'JSESSIONID-WYYY=2HPoD04WMJ%2FYE36xgaeWM7PSfqmNq0MVTIaxaxHwDEX5D%2BAACEURFg75eBEw%2BHTvTUDsw%2BaW73QTosP'
              '%2Bj5KUwGH4VEH4mB9AHggeBU3Q38a%2FZ%2BG7Q4gqb7GWQTiXuwrWmMEjfZfwm8sPk4BDeGsTgzw3T6TyTfiWkvMsMc1A1kJjuSqN'
              '%3A1530346387773; '
              '_iuqxldmzr_=32; __utma=94650624.320902977.1478443565.1526007372.1530344592.18; '
              '__utmb=94650624.2.10.1530344592; __utmc=94650624;'
              ' __utmz=94650624.1526007372.17.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic;'
              ' WM_TID=Zu7YRZX8MLxIvKteWvZKGZY4iTF7OW%2FE;'
              ' MUSIC_U=9de0b492647e4661e7bdf028ae8a486b297cdcadc988e86ecaab1ab402ce5de0857da9b612cf373654bc488418524552ff2a5e7544b3bf7b08c46f9844e112440d8f0d281b3ffd12;'
              ' __remember_me=true; __csrf=b2dc95628a83213f82ed97868b57a87c',
    'DNT': '1',
    'Host': 'music.163.com',
    'Pragma': 'no-cache',
    'Referer': 'http://music.163.com/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER'
}

# #设置 MongoDB的路径
# MONGO_URI = 'localhost'
# MONGO_DB = 'music163'
