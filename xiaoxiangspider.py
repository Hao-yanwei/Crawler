from bs4 import BeautifulSoup
from urllib import request
import os

class Spider(object):

    def __init__(self,url,path=''):
        self.url = url
        self.path = path

    # 配置环境
    def Runmain(self,url):
        req = request.urlopen(url)
        context = req.read().decode('UTF-8', 'replace')
        obj = BeautifulSoup(context, 'html5lib')
        self.first(obj)
    #爬取小说首页选取小说
    def first(self,obj):
        first = obj.find_all('h4')
        # print(first)
        f_read = first[0].a.get("href")
        news_web = f_read[6:12:1]
        new_web = "http://www.xxsy.net/partview/GetChapterList?bookid ="+news_web
        # print(new_web)
        self.main(new_web)
    #提取下一页内容
    def main(self,url):
        req = request.urlopen(url)
        context = req.read().decode('utf-8')
        obj = BeautifulSoup(context, 'html5lib')
        self.spider_book(obj)


    # 爬取页面章数
    def spider_book(self,obj):
        lis = obj.find_all('a')
        # print(lis)
        x = 0
        a = []
        for i in lis:
            web = i.get('href')
            # name = i.text
            # print(name)

            if web.endswith('html'):
                webs = 'http://www.xxsy.net'+web
                a.append(webs)
        print(a)
        while x < len(a):
            self.main_next(a[x])
            x += 1

    def main_next(self,url):
        req = request.urlopen(url)
        context = req.read().decode('utf-8')
        obj = BeautifulSoup(context, 'html5lib')
        self.write_book(obj)


    def write_book(self,obj):
        h = obj.find_all('h1')
        h1 = h[0].text
        self.save_book(h1)
        divs = obj.find_all('div',class_='chapter-main')
        p = divs[0].find_all('p')
        # print(p)
        for txt in p:
            txts = str(txt.text)
            self.save_book(txts)


    # 保存
    def save_book(self,obj):
        f = open(self.path,'a+',encoding='utf-8')
        f.write(obj+'\r\n')
        f.close()
        # pass

if __name__ == "__main__":
    url = 'http://www.xxsy.net/search?vip=0&sort=2'
    path = "E:/meinv/11处特工皇妃.txt"
    spr = Spider(url,path)
    spr.Runmain(url)
