from urllib import request
from bs4 import BeautifulSoup
from threading import Thread
import time
import os
from queue import Queue

q = Queue()
#运行代码
class ImgSpider(Thread):
    def __init__(self,url):
        self.url = url
        super().__init__()

    def get_page(self,url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safar'}
        head = request.Request(url, headers=headers)
        req = request.urlopen(head)
        context = req.read().decode("utf-8")
        if context:
            return context

    def run(self):
        global q

        while True:
            if q.qsize() < 50:
                context = self.get_page(self.url)
                obj = BeautifulSoup(context, 'html5lib')
                self.spiderImg(obj)
                self.nextpage(obj)
                self.run()
                time.sleep(0.5)

    def spiderImg(self,obj):
        imgs = obj.find_all('div',class_="page-content text-center")
        div = imgs[0].find_all('img')
        for img in div:
            src = img.get('data-original')
            print(src)
            q.put(src)


    """提取下一页网址"""
    def nextpage(self,obj):
        url = obj.find_all('ul',class_="pagination")
        lis = url[0].find_all('a',rel="next")
        href = lis[0].get('href')
        web = "https://www.doutula.com"+href
        self.url = web
        self.run()

class Saveimg(Thread):
    def run(self):
        name = 0
        global q
        while True:
            src = q.get()
            try:
                a = src[-4:]
                name1 = str(name) + a
                file = "E:/171125/爬虫/Headportrait/"
                # file = "./"
                path = os.path.join(file, name1)
                name += 1
                request.urlretrieve(src, path)
            except Exception as e:
                pass

            time.sleep(0.5)


if __name__ == "__main__":
    url = "https://www.doutula.com/photo/list/"
    file = "E:/171125/爬虫/Head portrait/"
    img = ImgSpider(url)
    save = Saveimg()
    img.start()
    save.start()
    img.join()
    save.join()



