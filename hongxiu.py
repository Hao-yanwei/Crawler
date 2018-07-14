# coding: utf-8
from urllib import request
from bs4 import BeautifulSoup
import os
import random

# req = request.urlopen(url)
# context = req.read().decode('utf-8')

class Httpequest(object):
    @staticmethod
    def urllibRequest(url):
        req = request.urlopen(url)
        if req.code == 200:
            context = req.read()
            return context

class ImgSpider(object):
    def __init__(self,imgurl='',spath='./'):
        self.imgurl = imgurl
        self.spath = spath
    def main(self,url):
        page = Httpequest.urllibRequest(url)
        if page:
            context = page.decode("utf-8","ignore")
            obj = BeautifulSoup(context, 'html5lib')
            # print(obj)

            self.spiderImg(obj)


    def saveImg(self,name,url):
        # path = os.path.join(self.spath, name)
        # # 保存到本地路径
        # request.urlretrieve(url, path)
         pass
    # 爬取页面
    def spiderImg(self,obj):
        # name = 0
        read = obj.find('a',class_='red-btn')
        a = read.get('href')
        a = 'http:'+a
        print(a)
        self.mainread(a)

    # 读取新网页
    def mainread(self, url):

        page = Httpequest.urllibRequest(url)
        if page:
            context = page.decode("utf-8")
            obj = BeautifulSoup(context, 'html5lib')
            self.startread(obj)
            # print(obj)

    # 开始阅读
    def startread(self,obj):
        txt = obj.find_all('div',class_='read-content')
        a = txt[0].children
        b =''
        for i in a:
            b+= str(i)+'\r\n'
        # print(b)
        c = b.replace('<p>',"")
        d = c.replace("</p>","")
        print(d)
        f = open('E:/爬虫/Head portrait/1.txt','w')
        f.write(d)
        f.close()

    def nextPage(self):
        pass

if __name__ == "__main__":
    url = "https://www.hongxiu.com/book/9006339503210703"
    file = "E:/爬虫/Head portrait/",
    get_img = ImgSpider(imgurl=url,spath=file)
    get_img.main(url)
