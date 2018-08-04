
-----------------
####爬取思路
1.分析页面，定义爬取字段
 2.观察网页，分析接口url，通过`xpath`和`json`解析爬取内容字段
 3.在`pipelines.py`写入存储方式
 4.开始爬取
---------------------
**1.分析网页，定义字段**

通过观察页面，我将字段分为了两块：一块为商品详情，包括价格名称，评论数量等等内容，另一块主要从商品得到评论，会员的相关信息，定义如下：

>   1.商品详情：
>   * link = scrapy.Field()  `商品链接`
>   * project_id = scrapy.Field()   `商品ID`
>   * name = scrapy.Field()  `商品名字`
>   * comment_num = scrapy.Field()  `评论人数`
>   * shop_name = scrapy.Field() `店家名字`
>   * price = scrapy.Field()  `价钱`
>   * GoodCountStr = scrapy.Field()  `好评`
>   * AfterCount = scrapy.Field() `中评`
>   * PoorCount = scrapy.Field()  `差评`

>   2.评论详情：
>   *  user_name = scrapy.Field()   `评论用户的名字`
>   * user_id = scrapy.Field()  `评论用户的ID`
>   * userProvince = scrapy.Field()  `评论用户来自的地区`
>   * content = scrapy.Field()  `评论内容`
>   * good_id = scrapy.Field()  `评论的商品ID`
>   * good_name = scrapy.Field() `评论的商品名字`
>   * date = scrapy.Field()   `评论时间`
>   *  replyCount = scrapy.Field()   `回复数`
>   *  score = scrapy.Field()  `评分`
>   *  status = scrapy.Field()  `状态`
>   *  userLevelId = scrapy.Field()  `用户等级`
>   *  productColor = scrapy.Field()  `商品颜色`
>   *  productSize = scrapy.Field()  `商品大小`
>   *  userLevelName = scrapy.Field()   `银牌会员，钻石会员等`
>   *  userClientShow = scrapy.Field()   `来自什么 比如来自京东客户端`
>   *  isMobile = scrapy.Field()  `是否来自手机`
 >   * days = scrapy.Field()  `天数`

####接口思路解析：

京东网页中的很多数据是写在js中的，需要在network中查找接口路由，从而获得其真正所在的url地址，通过不同的id与接口组合得到不同的解析内容，分析如下：
######分析接口：
![商品价格接口分析.png](https://upload-images.jianshu.io/upload_images/6591571-a28ffbbbd7aea80d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###### 京东价格js接口url:   `https://p.3.cn/prices/mgets?callback=jQuery8876824&skuIds=J_4471753`

![Image 5.png](https://upload-images.jianshu.io/upload_images/6591571-72733409e37e7d3e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###### 京东评论数量js接口url:   `https://club.jd.com/comment/productCommentSummaries.action?referenceIds=4471753`

![Image 6.png](https://upload-images.jianshu.io/upload_images/6591571-f150567ffed57ab0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###### 京东评论js接口url:   `https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv2394&productId=6023682&score=0&sortType=5&page=2&pageSize=10&isShadowSku=0&fold=1`
----------------


####存入Mysql数据库
![商品详情.png](https://upload-images.jianshu.io/upload_images/6591571-f63b55bd8e935ddc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![评论详情 2.png](https://upload-images.jianshu.io/upload_images/6591571-e35cba5575ea6fa6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

