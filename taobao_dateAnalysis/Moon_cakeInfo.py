# -*- coding: utf-8 -*-
import re
import xlwt
import time
import pandas as pd
from retrying import retry
from concurrent.futures import ThreadPoolExecutor
import matplotlib
# %matplotlib inline


# 计时开始
start = time.clock()
# plist 为1-100页的URL的编号num
plist = []
for i in range(1, 101):
    j = 44 * (i-1)
    plist.append(j)

listno = plist
datatmsp = pd.DataFrame(columns=[])

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'

}


# 设置最大重试次数
# @retry(stop_max_attempt_number = 8)


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
            price = eval(plt[i].split(':')[1]) # 价格
            title = eval(tlt[i].split(':')[1])  # 标题
            location = eval(loc[i].split(':')[1])  # 地域
            location = location.split(' ')[0]
            sales = eval(sale[i].split(':')[1])  # 销量
            sales = re.match(r'\d+',sales).group(0)
            print(price)
            with open("月饼数据.txt",'a',encoding='utf-8') as f:
                print(f)
                f.write(title+','+price+','+sales+','+location+'\n')
    except Exception as e:
        print(e)


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
        except Exception as e:
            print(e)
            continue
if __name__ == "__main__":
    main()
