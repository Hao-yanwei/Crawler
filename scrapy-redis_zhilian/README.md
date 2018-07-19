
scrapy-redis [官方github地址](https://github.com/rmax/scrapy-redis)

## 1， scrapy-redis的简单理解

Scrapy 是一个通用的爬虫框架，但是不支持分布式，Scrapy-redis是为了更方便地实现Scrapy分布式爬取，而提供了一些以redis为基础的组件(仅有组件)。

安装：`pip install scrapy-redis`

Scrapy-redis提供了下面四种组件（components）：(四种组件意味着这四个模块都要做相应的修改)

- 1.  Scheduler（队列）
- 2.  Duplication Filter （去重）
- 3.  Item Pipeline（将Item存储在redis中以实现分布式处理）
- 4.  Base Spider

**Scheduler：**

Scrapy改造了python本来的collection.deque(双向队列)形成了自己的Scrapy queue(https://github.com/scrapy/queuelib/blob/master/queuelib/queue.py)，
但是Scrapy多个spider不能共享待爬取队列Scrapy queue， 即Scrapy本身不支持爬虫分布式，scrapy-redis 的解决是把这个Scrapy queue换成redis数据库（也是指redis队列），从同一个redis-server存放要爬取的request，便能让多个spider去同一个数据库里读取。

Scrapy中跟“待爬队列”直接相关的就是调度器Scheduler，它负责对新的request进行入列操作（加入Scrapy queue），取出下一个要爬取的request（从Scrapy queue中取出）等操作。它把待爬队列按照优先级建立了一个字典结构，比如：

    {
       -优先级0 : 队列0
       -优先级1 : 队列1
       -优先级2 : 队列2
    }

然后根据request中的优先级，来决定该入哪个队列，出列时则按优先级较小的优先出列。为了管理这个比较高级的队列字典，Scheduler需要提供一系列的方法。但是原来的Scheduler已经无法使用，所以使用Scrapy-redis的scheduler组件。

**Duplication Filter：**

Scrapy中用集合实现这个request去重功能，Scrapy中把已经发送的request指纹放入到一个集合中，把下一个request的指纹拿到集合中比对，如果该指纹存在于集合中，说明这个request发送过了，如果没有则继续操作。

在scrapy-redis中去重是由Duplication Filter组件来实现的，它通过redis的set 不重复的特性，巧妙的实现了Duplication Filter去重。scrapy-redis调度器从引擎接受request，将request的指纹存⼊redis的set检查是否重复，并将不重复的request push写⼊redis的 request queue。

引擎请求request(Spider发出的）时，调度器从redis的request queue队列⾥里根据优先级pop 出一个request 返回给引擎，引擎将此request发给spider处理。

**Item Pipeline：**

引擎将(Spider返回的)爬取到的Item给Item Pipeline，scrapy-redis 的Item Pipeline将爬取到的 Item 存⼊redis的 items queue。

修改过Item Pipeline可以很方便的根据 key 从 items queue 提取item，从⽽实现 items processes集群。

**Base Spider**

不在使用scrapy原有的Spider类，重写的RedisSpider继承了Spider和RedisMixin这两个类，RedisMixin是用来从redis读取url的类。

当我们生成一个Spider继承RedisSpider时，调用setup_redis函数，这个函数会去连接redis数据库，然后会设置signals(信号)：

一个是当spider空闲时候的signal，会调用spider_idle函数，这个函数调用schedule_next_request函数，保证spider是一直活着的状态，并且抛出DontCloseSpider异常。

一个是当抓到一个item时的signal，会调用item_scraped函数，这个函数会调用schedule_next_request函数，获取下一个request。

**Scrapy-Redis分布式策略：**

假设有四台电脑：Windows 10、Mac OS X、Ubuntu 16.04、CentOS 7.2，任意一台电脑都可以作为 Master端 或 Slaver端，比如：
Master端(核心服务器) ：使用 Windows 10，搭建一个Redis数据库，不负责爬取，只负责url指纹判重、Request的分配，以及数据的存储
Slaver端(爬虫程序执行端) ：使用 Mac OS X 、Ubuntu 16.04、CentOS 7.2，负责执行爬虫程序，运行过程中提交新的Request给Master
首先Slaver端从Master端拿任务（Request、url）进行数据抓取，Slaver抓取数据的同时，产生新任务的Request便提交给 Master 处理；
Master端只有一个Redis数据库，负责将未处理的Request去重和任务分配，将处理后的Request加入待爬队列，并且存储爬取的数据。
![图片1.png](https://upload-images.jianshu.io/upload_images/6591571-0aa3ae1f42aae80d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

----------------------------------------
######核心参数
`settings.py`
```
# ===========================================================================
#启用Redis调度存储请求队列
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

#确保所有的爬虫通过Redis去重
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

#默认请求序列化使用的是pickle 但是我们可以更改为其他类似的。PS：这玩意儿2.X的可以用。3.X的不能用
#SCHEDULER_SERIALIZER = "scrapy_redis.picklecompat"

#不清除Redis队列、这样可以暂停/恢复 爬取
#SCHEDULER_PERSIST = True

#使用优先级调度请求队列 （默认使用）
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'
#可选用的其它队列
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.LifoQueue'

#最大空闲时间防止分布式爬虫因为等待而关闭
#这只有当上面设置的队列类是SpiderQueue或SpiderStack时才有效
#并且当您的蜘蛛首次启动时，也可能会阻止同一时间启动（由于队列为空）
#SCHEDULER_IDLE_BEFORE_CLOSE = 10

#将清除的项目在redis进行处理
ITEM_PIPELINES = {
    'scrapy_redis.pipelines.RedisPipeline': 300
}

#序列化项目管道作为redis Key存储
#REDIS_ITEMS_KEY = '%(spider)s:items'

#默认使用ScrapyJSONEncoder进行项目序列化
#You can use any importable path to a callable object.
#REDIS_ITEMS_SERIALIZER = 'json.dumps'

#指定连接到redis时使用的端口和地址（可选）
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

#指定用于连接redis的URL（可选）
#如果设置此项，则此项优先级高于设置的REDIS_HOST 和 REDIS_PORT
#REDIS_URL = 'redis://user:pass@hostname:9001'

#自定义的redis参数（连接超时之类的）
#REDIS_PARAMS  = {}

#自定义redis客户端类
#REDIS_PARAMS['redis_cls'] = 'myproject.RedisClient'

#如果为True，则使用redis的'spop'进行操作。
#如果需要避免起始网址列表出现重复，这个选项非常有用。开启此选项urls必须通过sadd添加，否则会出现类型错误。
#REDIS_START_URLS_AS_SET = False

#RedisSpider和RedisCrawlSpider默认 start_usls 键
#REDIS_START_URLS_KEY = '%(name)s:start_urls'

#设置redis使用utf-8之外的编码
#REDIS_ENCODING = 'latin1'

```
`spider`
```
from scrapy_redis.spiders import RedisCrawlSpider

class Spider(RedisCrawlSpider):#继承scrapy-redis中定义好的类
    pass
```
****
注释：
> * 1. 当使用分布式爬虫爬取数据时，要保证redis数据库例远程之间可以连接
> * 2. Master端和Slaver端要使用统一的redis数据库保证项目的连接使用
> * 3. 在Linux中配置Master端，修改配置文件 redis.conf，打开redis.conf配置文件，示例:linux系统: `sudo vi /etc/redis/redis.conf`,Master端`redis.conf`里注释`bind 127.0.0.1`，Slave端才能远程连接到Master端的Redis数据库。如果要把当前电脑当成Master端把`bind 127.0.0.1`注释掉，如果是Slaver端可以不修改
> * 4. `redis.conf`中`daemonize`配置
  `daemonize no`表示Redis默认不作为守护进程运行，即在 运行`redis-server /etc/redis/redis.conf`时，将显示Redis 启动提示画面；`daemonize yes`则默认后台运行，不必重新启动新的终端窗口执行其他命令，看个人喜好和实际需
> * 5.  Linux中启动redis服务
推荐指定配置文件启动
`sudo redis-server /etc/redis/redis.conf`或者`sudo service redis start`
> * 6.  Linux中停止redis服务
`sudo kill -9 redis的进程id`或者`sudo service redis stop`
> * 7. Linux中重启redis服务
`sudo service redis restart`
  当配置文件重新配置后，一般会重启服务器这样配置才生效
> * 8. 保证存储数据库之间的连接，当master和slaver端要同时存入master端的mysql数据库，要保证slaver端是否可以连接master端的数据库
> * 9.  [windows下远程连接Mysql](https://www.cnblogs.com/fnlingnzb-learner/p/5848405.html)
> * 10. 在Ubuntu16.04下安装mysql：https://blog.csdn.net/xiangwanpeng/article/details/54562362

本文参考链接：https://cuiqingcai.com/4048.html




