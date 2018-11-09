# 用Python分析月饼之王花落谁手



但愿人长久
王菲 - 菲靡靡之音


中秋佳节，除了假日团圆，月饼也是头巷尾的话题焦点今年中秋，谁的月饼呼声最高？什么口味的月饼虽受欢迎？

我将与你一起爬取淘宝网全网月饼销售数据，再经过数据分析，告诉你今年谁是“月饼之王”。不过在爬取数据与分析数据之前，插播一段月饼历史之情。

## 一、月饼的历史
![image](http://upload-images.jianshu.io/upload_images/6591571-c765e2aca17a4a43?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

据说早在殷周时期，江浙一带就有一种纪念太师闻仲的边薄心厚的“太师饼”，可以说是月饼的祖宗了。至于为什么要纪念闻仲，我也不知道。


后来到了北宋，被皇家看上了，在中秋节那天吃，不得不说皇室贵族的宣传力度果然是一般人的十倍以上，为月饼的传播起了跨世纪的作用。

贵族们一看这玩意火了，得蹭个热点，那给它们取个名字吧，于是想了个大名叫“月团”，小名叫“小饼”，我说你们为啥就不能把这两个名字合并一下？

至于月饼这个名字，是直到南宋时期才第一次出现在书里的。后面大概就是月饼一步一步凭借自己的努力渐渐站在中秋节身边的励志故事了。

众所周知：传统的中国四大月饼包括，广式月饼，京式月饼，苏式月饼和潮式月饼。现在随着时代的发展，也出现了好多新种类，比如冰皮月饼、海味月饼、冰淇淋月饼等等。

## 二、数据获取

我就以淘宝网上的月饼为目标，来获取最近全国各地近段时间月饼销售情况。（目标链接：https://s.taobao.com/search?q=月饼）



工具&模块：
工具：Python3.7+Sublime Text
模块：requests、jieba、matplotlib、wordcloud、imread、pandas、numpy 等。

目的主要是通过对数据的分析，来看看不同关键词word对应的sales的统计、月饼价格以及销量的分布情况、以及不同省份的月饼销量情况。

详情代码如下：
```
import requests
import re

#下载网页
def get_html_text(url):
    try:
        res = requests.get(url,timeout=30)
        res.raise_for_status()
        res.encoding = res.apparent_encoding
        return res.text
    except:
        return ""

#解析网页并保存数据    
def parse_page(html):
    try:
        plt = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html) 
        tlt = re.findall(r'\"raw_title\"\:\".*?\"', html)
        loc = re.findall(r'\"item_loc\"\:\".*?\"', html)
        sale = re.findall(r'\"view_sales\"\:\".*?\"', html)
        #print(plt)
        for i in range(len(plt)):
        	price = eval(plt[i].split(':')[1])
        	title = eval(tlt[i].split(':')[1])
        	location = eval(loc[i].split(':')[1])
        	location = location.split(' ')[0]
        	sales = eval(sale[i].split(':')[1])
        	sales = re.match(r'\d+',sales).group(0)
        	print(price)
        	with open("月饼数据.txt",'a',encoding='utf-8') as f:
        		print(f)
        		f.write(title+','+price+','+sales+','+location+'\n')
    except:
    	print("")


def main():
	goods="月饼"
	depth=100
	start_url = 'https://s.taobao.com/search?q=' + goods
	for i in range(depth):
		try:
			url = start_url + '&s=' + str(44 * i)
			print('url=',url)
			html = get_html_text(url)
			parse_page(html)
		except:
			continue

main()
```
知识点：Response对象的属性

- r.status_code HTTP请求的返回状态，200表示连接成功，404表示失败 ；
- r.text HTTP响应内容的字符串形式，即url对应的页面内容；
- r.encoding 从HTTP header中猜测的响应内容编码方式；
- r.apparent_encoding 从内容中分析出的响应内容编码方式（备选编码方式）；

## 三、数据清洗预览
![image](http://upload-images.jianshu.io/upload_images/6591571-756ce18df9b2281a?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


由上图可以看出，全网月饼的均价在90元左右，最贵月饼价高达9999元，最高销量为355444（数据为当前爬取数据为准）

## 四、数据分析可视化

广式月饼风采依旧，蛋黄、莲蓉口味深受最爱



结论：

广式月饼、礼盒装占比很高；从口味上来看，蛋黄口味占比很高，比莲蓉，五仁都高，其他口味豆沙、水果、火腿等次之；从品牌商家来看，北京稻香村、广东华美排名靠前；从礼盒装、企业、员工、团购、批发来看，淘宝网也是企业采购月饼送员工的渠道之一。

详情代码如下：
```
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib
from pyecharts import Geo,Style,Line,Bar,Overlap
from wordcloud import WordCloud, ImageColorGenerator
from os import path
from pylab import mpl
import jieba

f = open(r"C:\Users\Administrator\Desktop\月饼数据.txt",encoding='utf-8')

df = pd.read_csv(f,sep=',',names=['title','price','sales','location'])

title = df.title.values.tolist()

#对每个标题进行分词
title_s = []

for line in title:
	title_cut = jieba.lcut(line)
	title_s.append(title_cut)

title_clean = []

#停用词表
stopwords = ["月饼","礼品","口味","礼盒","包邮","【","】","送礼","大",
"中秋节","中秋月饼","2","饼","蓉","多","个","味","斤","送"," ","老",
"北京","云南","网红老"]


#剔除停用词表
for line in title_s:
	line_clean = []
	for word in line:
		if word not in stopwords:
			line_clean.append(word)
	title_clean.append(line_clean)

title_clean_dist = []

#进行去重
for line in title_clean:
	line_dist = []
	for word in line:
		if word not in line_dist:
			line_dist.append(word)
	title_clean_dist.append(line_dist)

allwords_clean_dist = []
for line in title_clean_dist:
	for word in line:
		allwords_clean_dist.append(word)

df_allwords_clean_dist = pd.DataFrame({'allwords':allwords_clean_dist})

#对过滤_去重词语进行汇总统计
word_count = df_allwords_clean_dist.allwords.value_counts().reset_index()
word_count.columns = ['word','count']

backgroud_Image = plt.imread('1.jpg')

wc = WordCloud(width=1024,height=768,background_color='white',

	mask=backgroud_Image,font_path="C:\simhei.ttf",max_font_size=400,
	random_state=50)

wc = wc.fit_words({x[0]:x[1] for x in word_count.head(100).values})

plt.imshow(wc,interpolation='bilinear')
plt.axis("off")
plt.show()

d = path.dirname(__file__)

wc.to_file(path.join(d,"yuebing.png"))
```
![image](http://upload-images.jianshu.io/upload_images/6591571-4b343f10a64f446c?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
`知识点：`

font_path : string //字体路径，需要展现什么字体就把该字体路径+后缀名写上，如：font_path = '黑体.ttf'；
mask : nd-array or None (default=None) //如果参数为空，则使用二维遮罩绘制词云。如果 mask 非空，设置的宽高值将被忽略，遮罩形状被 mask 取代。 除全白（#FFFFFF）的部分将不会绘制，其余部分会用于绘制词云。如：bg_pic = imread('读取一张图片.png')， 背景图片的画布一定要设置为白色（#FFFFFF），然后显示的形状为不是白色的其他颜色。可以用ps工具将自己要显示的形状复制到一个纯白色的画布上再保存，就ok了；
stopwords : set of strings or None //设置需要屏蔽的词，如果为空，则使用内置的STOPWORDS ；
background_color : color value (default=”black”) //背景颜色，如background_color='white',背景颜色为白色； 
max_font_size : int or None (default=None) //显示的最大的字体大小 ；
fit_words(frequencies) //根据词频生成词云（frequencies，为字典类型）

不同关键词word对应的sales之和的统计分析

（说明：例如 词语 ‘广式’，则统计商品标题中含有‘广式’一词的商品的销量之和，即求出具有‘广式’风格的商品销量之和）


由上图可以看出：礼盒装、广式、蛋黄、莲蓉、五仁、稻香村、华美等关键词靠前，也再次验证了广式月饼堪称月饼之王，实际付款人高达近700万，广式月饼可谓是风采依旧。虽然广式月饼起源于广州，但凭借其松软的饼皮和多元丰富的馅料，实际已经在全国各地流行开来，成为名副其实的“月饼之王”。

详情代码如下：
```
w_s_sum = []
for w in word_count.word:
	i = 0
	s_list = []
	for t in title_clean_dist:
		if w in t:
			s_list.append(df.sales[i])
		i+= 1
	w_s_sum.append(sum(s_list))

df_w_s_sum = pd.DataFrame({'w_s_sum':w_s_sum})
df_word_sum = pd.concat([word_count,df_w_s_sum],axis=1,ignore_index=True)
df_word_sum.columns = ['word','count','w_s_sum']
df_word_sum.sort_values('w_s_sum',inplace=True,ascending=True)
df_w_s = df_word_sum.tail(30)

attr = df_w_s['word']
v1 = df_w_s['w_s_sum']

bar = Bar("月饼关键词销量分布图")

bar.add("关键词",attr,v1,is_stack=True,xaxis_rotate=30,yaxix_min=4.2,

    xaxis_interval=0,is_splitline_show=False)

overlap = Overlap()

overlap.add(bar)

overlap.render('月饼关键词_销量分布图.html')
```

多数商品销量为3000以下，占比高达90%


由上图看出，销售量在10万以上的寥寥无几，共8种，其中销售量30万以上就有6款。当今网红经济下，爆品为王，一款独大；正所谓网红就是营销，爆品就是产品，有了好的产品再经过营销的运作就能产生十倍的放大效益， 如果没有好的产品，光有营销企业也难以长久。要利用网红经济来打造爆款，选择爆款一定要有自己的特色，在销售的过程中，客户的评价对产品的搜索排序和客户下单转化起着至关重要的作用；

消费降级？均价在10-100元占比50%


商品数量随着价格总体呈现下降阶梯形势，价格越高，在售的商品越少；低价位商品居多，价格在10-100之间的商品最多，100-200之间的次之，价格8000以上的商品较少。

详情代码如下：
```
f = open(r"C:\Users\Administrator\Desktop\月饼数据.txt",encoding='utf-8')

df = pd.read_csv(f,sep=',',names=['title','price','sales','location'])

print(df.sort_values(by='price'))

price_info = df[['price','location']]

bins = [0,10,50,100,150,200,300,500,1000,5000,8000]
level = ['0-10','10-50', '50-100','100-150' ,'150-200', '200-500','500-1000','1000-5000','5000-8000','8000以上']

price_stage = pd.cut(price_info['price'], bins = bins,labels = level).value_counts().sort_index()
print(price_stage)

attr = price_stage.index
v1 = price_stage.values

bar = Bar("价格区间&月饼种类数量分布")
bar.add("",attr,v1,is_stack=True,xaxis_rotate=30,yaxix_min=4.2,
    xaxis_interval=0,is_splitline_show=False)

overlap = Overlap()
overlap.add(bar)
overlap.render('价格区间&月饼种类数量分布.html')

```
后记：



由上图可看出，全网Top15中，广式口味占80%，全国各地都在卖广式月饼。月饼种类那么多，为何偏偏是广式月饼横行中国？广式月饼外层是糖浆皮，以小麦粉、糖浆、植物油、碱水等原料制作烘烤而成，这并非中国传统的糕饼技艺，这与广式月饼的起源有关。广东流行中秋月饼比中国其他地区的时间更晚，要迟到晚清时期。在此之前，广州沙面地区已因鸦片战争变为英、法租界，各类西饼店纷纷踏上广州地界。以糖浆皮包裹烘烤而成的广式月饼，其实是学习西式糕点作法的产物。


广式月饼能一统天下，最重要的一条是广式月饼的原料，这个原料就是莲蓉。早在1889年，当时广州城西的一家叫“莲香楼”的糕酥店，将莲子熬成莲蓉作馅料，做成的酥饼清香可口，大受欢迎。后来，莲香楼的生产者将这种莲蓉馅料的饼点定型为月饼，逐渐形成后来的广式月饼。

今年你吃到哪些好吃的月饼了吗？

