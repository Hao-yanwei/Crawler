# coding: utf-8
from urllib import request
from bs4 import BeautifulSoup
import os
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
        self.num=1

    def main(self, url):
        page = Httpequest.urllibRequest(url)

        if page:
            # print('111')
            context = page.decode('utf-8')
            obj = BeautifulSoup(context, 'html5lib')
            self.spiderImg(obj)

    def saveImg(self,name,url):
        spath = "E:/爬虫/meinv/"
        path = os.path.join(spath, name)

        # 抛出异常
        try:
            # 保存到本地路径
            request.urlretrieve(url,path)
        except Exception as e:
            pass

    def spiderImg(self,obj):
        name = 0
        img = obj.find_all('img')
        for tag in img:
            new_tag = tag.attrs['src']
            # print(new_tag)
            if new_tag.endswith('jpg'):
                name1 = str(name)+'.jpg'
                self.saveImg(name1,new_tag)
                name +=1
                # print(name1)
            else:
                continue
        # 爬取下一页
        self.nextPage(obj)

    # 下一页地址
    def nextPage(self,obj):
        # li = obj.find_all('li', class_='next')
        # find_a = li[0].a.get('href')
        # print(find_a)
        # 将网址导入到解析页main方法中
        i = 1
        while i:
            web = 'https://tp.388g.com/xiezhen/51_' + str(i)+ '.html'
            print(web)
            self.main_next(web)
            i += 1
    # 调用解析网页的方法
    def main_next(self,url):
        req = request.urlopen(url)
        context = req.read().decode('utf-8')
        obj = BeautifulSoup(context, 'html5lib')
        self.getPages(obj)
     # 获取爬取img链接  
    def getPages(self,obj):
        # print('11111')
        jpg = []
        imgs = obj.find_all('img')

        for img in imgs:
            src = img.get('src')
            # print(src)
            jpg.append(src)
        # 删除列表最后一项
        jpg.pop()
        # 为图片取名并调用下载方法
        for x in jpg:
            name1 = str(self.num) + '.jpg'
            self.saveImg(name1, x)
            self.num += 1
            print(name1)

if __name__ == "__main__":
    url = "https://tp.388g.com/xiezhen/"
    file = "E:/爬虫/meinv/"
    get_img = ImgSpider(imgurl=url,spath=file)
    get_img.main(url)
