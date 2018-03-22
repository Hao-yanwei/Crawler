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
    def main(self,url):
        page = Httpequest.urllibRequest(url)
        if page:
            context = page.decode("utf-8","ignore")
            obj = BeautifulSoup(context, 'html5lib')
            # print(obj)
            self.spiderImg(obj)


    def saveImg(self,name,url):
        spath = "E:/171125/爬虫/Head portrait/"
        path = os.path.join(spath, name)
        # 保存到本地路径
        request.urlretrieve(url, path)

    def spiderImg(self,obj):
        name = 0
        img = obj.find_all('img')
        # print(img)
        for tag in img:
            new_tag = tag.attrs['src']
            # print(new_tag)
            if new_tag.endswith('jpg'):
                name1 = str(name)+'.jpg'
                self.saveImg(name1,new_tag)
                name +=1
                print(name1)
            else:
                continue


    def nextPage(self):
        pass
if __name__ == "__main__":
    url = "https://www.qqtn.com/article/article_103358_1.html"
    file = "E:/171125/爬虫/Head portrait/",
    get_img = ImgSpider(imgurl=url)
    get_img.main(url)
