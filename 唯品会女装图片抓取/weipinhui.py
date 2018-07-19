# coding=utf-8
# 导入selenium的浏览器驱动接口
import os
from urllib import request

from selenium import webdriver
# 要想调用键盘按键操作需要引入keys包
from selenium.webdriver.common.keys import Keys
# 导入chrome选项
from selenium.webdriver.chrome.options import Options
# 创建chrome浏览器驱动，无头模式
import time
from bs4 import BeautifulSoup



class ImageSpider(object):

    def run(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        self.page(driver)

    def page(self, driver):
        # 请求唯品会页面
        driver.get(
            "https://category.vip.com/search-3-0-1.html?q=3|30036||&rp=30074|30063&ff=women|0|2|2&adidx=1&f=ad&adp=65001&adid=326630")
        time.sleep(3)

        # 逐渐滚动浏览器窗口，令ajax逐渐加载
        for i in range(1, 10):
            # js = "var q=document.body.scrollTop=" + str(500 * i)  # PhantomJS
            js = "var q=document.documentElement.scrollTop=" + str(500 * i)  # 谷歌 和 火狐

            driver.execute_script(js)
            time.sleep(3)
            # 拿到页面源码
            data = driver.page_source
            # 将文件通过bs4的方式解析
            soup = BeautifulSoup(data, 'lxml')
            self.parsing(soup)

    def parsing(self, soup):
        imgs = soup.find_all("div", class_="goods-image")
        for i in imgs:
            src = i.find_all("img")[0].get("src")
            num = src[-10:]
            jpg = "http:" + src
            self.saveImg(num,jpg)

    def saveImg(self,name,url):
        spath = "D:\study\python\workspace\imgs"
        path = os.path.join(spath, name)
        print(url)
        print("==============")
        print(path)
        # 抛出异常
        try:
            # 保存到本地路径
            request.urlretrieve(url,path)
        except Exception as e:
            pass


if __name__ == '__main__':
    main = ImageSpider()
    main.run()
