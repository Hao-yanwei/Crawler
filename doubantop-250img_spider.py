from urllib import request
import re
import os
# url = "https://movie.douban.com/top250"

class httpRequest(object):
    @staticmethod
    def urllibrequest(url):
        req = request.urlopen(url)
        if req.code == 200:
            context = req.read()
            return context


class doubanSpider(object):
    def __init__(self,spath = './',beseurl=''):
        self.spath = spath
    def startReqUrl(self,url):
        page = httpRequest.urllibrequest(url)
        if page:
            context = page.decode("utf-8")
            self.parsePage(context)
            nexturl = self.getNextPage(context)
            if nexturl:
                self.startReqUrl(nexturl)
    # 保存图片
    def saveImg(self,name,url):
        # 路径拼接
        path = os.path.join(self.spath,name)
        # 保存
        request.urlretrieve(url,path)
    # 爬取页面
    def parsePage(self,obj):
        if obj:
            # h5页面寻找标签
            listDiv = re.findall(r'<div class="item">.*?</div>', obj, re.S)
            if listDiv:
                for div in listDiv:
                    # 文件名拼接
                    result = re.search(r'alt="(.*?)" src="(.*?)" ', div)
                    if result:
                        name,url = result.groups()
                        # print(name, url)
                        # 倒着切割
                        tail = url.rsplit('.',1)[1]
                        name += '.'+tail
                        self.saveImg(name,url)
                        print(result)
                    break
    #获取下一页
    def getNextPage(self,obj):
        if obj:
            nextpage = re.search('<span class="next">.*?</span>', obj, re.S)
            if nextpage:
                nexturl = re.search(r'<a href = "(.*?)" ', nextpage.group())
                if nexturl:

                    url = nexturl.groups()[0]
                    print(url)
                    if url:
                        return self.beseurl+url



if __name__ == "__main__":
    requrl = "https://movie.douban.com/top250"
    d =doubanSpider(spath="E:/171125/爬虫/img/",
                               beseurl='requrl')
    d.startReqUrl(requrl)
    d.getNextPage("https://movie.douban.com/top250")
