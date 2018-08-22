import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
import time
import pymongo

client = pymongo.MongoClient('localhost')
db = client['Taobao']

def save_to_mongo(info):
    try:
        if db['TaobaoBra'].insert(info):
            print('成功保存',info)
        else:
            print('保存失败',info)
    except Exception:
        print('出现错误！')

def get_html(url):
    headers={
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'zh-CN,zh;q=0.9',
        'cookie':'cna=llA7E8brPBoCAbcOHNi7hVAV; '
                 'hng=CN%7Czh-CN%7CCNY%7C156; '
                 'enc=ccE6LTKXBdwRHQ7N5jkpqIncgJ8ZidJyveRceAa64P6DhYJ6QMkyjWBtepCyjBNyG%2FmTUxsaCkoA3N0FfKOV%2Fw%3D%3D; '
                 'dnk=%5Cu4E00%5Cu661F%5Cu4EAE%5Cu51490513; '
                 'uc1=cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&cookie21=URm48syIYB3rzvI4Dim4&cookie15=VFC%2FuZ9ayeYq2g%3D%3D&existShop=false&pas=0&cookie14=UoTeOL8cjQtVEQ%3D%3D&tag=8&lng=zh_CN; '
                 'uc3=nk2=saDJ046ugXS34yQY&id2=UoH7LXG%2BMalBgg%3D%3D&vt3=F8dBz49%2Bydi31ITh4yc%3D&lg2=UIHiLt3xD8xYTw%3D%3D; '
                 'tracknick=%5Cu4E00%5Cu661F%5Cu4EAE%5Cu51490513;'
                 ' lid=%E4%B8%80%E6%98%9F%E4%BA%AE%E5%85%890513; '
                 '_l_g_=Ug%3D%3D; unb=1046201742;'
                 ' lgc=%5Cu4E00%5Cu661F%5Cu4EAE%5Cu51490513;'
                 ' cookie1=AHsrZpxv627ntESz%2F7ugNTH0xuQ4fdykpEPu2%2B73a%2Bw%3D;'
                 ' login=true; '
                 'cookie17=UoH7LXG%2BMalBgg%3D%3D; '
                 'cookie2=2294a1373e40fa7af38ee22f09db4dd0; '
                 '_nk_=%5Cu4E00%5Cu661F%5Cu4EAE%5Cu51490513;'
                 ' t=5fae17de501fc8266e8bf1c512a1ffed; '
                 'sg=328; csg=d3101850; _'
                 'tb_token_=ee54ee8ebbeaf; '
                 'cq=ccp%3D0; '
                 'isg=BJycJ7PqKlE43d6yWQjQlkJfbbqOvUfdUCCvKXadoAdqwTxLniUQzxJTJSk58niXif-none-match: W/"dC4RnOtm6Ix4vk0qQNVjQQ=="',
        'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
    }
    response=requests.get(url,headers=headers)
    return response.text

def get_id(href):
    product_url = 'https:' + href
    product_html = get_html(product_url)
    itemId = re.search('id=(.*?)&', product_url, re.S).group(1)
    sellerId = re.search('&user_id=(.*?)&', product_url, re.S).group(1)
    spuId = re.search('&spuId=(.*?)&', product_html, re.S).group(1)
    return itemId,sellerId,spuId

def get_rate(url):
    html=get_html(url)
    soup=BeautifulSoup(html,'lxml')
    products=soup.select('.product .productImg-wrap a')
    for product in products:
        href = product.attrs['href']
        itemId, sellerId, spuId=get_id(href)
        page=get_page(spuId,itemId,sellerId)
        for i in range(1,page+1):
            detail=get_info(spuId,itemId,sellerId,i)
            rateList = detail['rateDetail']['rateList']
            for j in range(len(rateList)):
                info={
                    'id':rateList[j]['id'],
                    'auctionSku':rateList[j]['auctionSku'],
                    'rateContent':rateList[j]['rateContent']
                }
                time.sleep(1)
                save_to_mongo(info)

##得到每件商品对应评论的页码数
def get_page(spuId,itemId,sellerId):
    url='https://rate.tmall.com/list_detail_rate.htm?itemId='+itemId+'&spuId='+spuId+'&sellerId='+sellerId+'&order=3&currentPage=1&append=0&content=1&tagId=&posi=&picture=&ua=098%23E1hvovvnvpvvUvCkvvvvvjiPPFdpgjtPPFdhljYHPmPOAj1UPsSU0jEjPLFh0jiU9phvHnsGvH6DzYswSEGr7%2FafzUSwqHiIdphvmpvhtOjo631QAu6CvCWICE0vvQWw8R%2BidTpro9eYSah6iQhvCvvv9UUPvpvhvv2MMQyCvhQWIMwvC0q6D7zhVTtML%2BFy6Wva5ja2gb2XSfpAOH2%2BFOcn%2B3C1B%2FFEDaVTRogRD7zUQ8TJEcqwa70xdBDAbz79D76XV366%2B8c6D46XKphv8vvvvvCvpvvvvvmm86CvvHIvvUUdphvWvvvv9krvpv3Fvvmm86CvmVRivpvUvvmv%2BoesW5kEvpvVmvvC9jX2vphvC9v9vvCvp2yCvvpvvvvv3QhvCvvhvvvtvpvhvvvvvv%3D%3D&isg=BKys9pU-2oNQoM4jz7aXsgZyfYoezVFq9rv68wbt1tf_EU0bLnSGnyvDNdmpnohn&needFold=0&_ksTS=1526485595603_2406&callback=jsonp2407'
    html = get_html(url)
    html=html.replace('jsonp2407(','')
    html=html.replace(')','')
    detail = json.loads(html)
    page = detail['rateDetail']['paginator']['lastPage']
    return int(page)

def get_info(spuId,itemId,sellerId,page):
    url='https://rate.tmall.com/list_detail_rate.htm?itemId='+itemId+'&spuId='+spuId+'&sellerId='+sellerId+'&order=3&currentPage='+str(page)+'&append=0&content=1&tagId=&posi=&picture=&ua=098%23E1hvovvnvpvvUvCkvvvvvjiPPFdpgjtPPFdhljYHPmPOAj1UPsSU0jEjPLFh0jiU9phvHnsGvH6DzYswSEGr7%2FafzUSwqHiIdphvmpvhtOjo631QAu6CvCWICE0vvQWw8R%2BidTpro9eYSah6iQhvCvvv9UUPvpvhvv2MMQyCvhQWIMwvC0q6D7zhVTtML%2BFy6Wva5ja2gb2XSfpAOH2%2BFOcn%2B3C1B%2FFEDaVTRogRD7zUQ8TJEcqwa70xdBDAbz79D76XV366%2B8c6D46XKphv8vvvvvCvpvvvvvmm86CvvHIvvUUdphvWvvvv9krvpv3Fvvmm86CvmVRivpvUvvmv%2BoesW5kEvpvVmvvC9jX2vphvC9v9vvCvp2yCvvpvvvvv3QhvCvvhvvvtvpvhvvvvvv%3D%3D&isg=BKys9pU-2oNQoM4jz7aXsgZyfYoezVFq9rv68wbt1tf_EU0bLnSGnyvDNdmpnohn&needFold=0&_ksTS=1526485595603_2406&callback=jsonp2407'
    html = get_html(url)
    html = html.replace('jsonp2407(', '')
    html = html.replace(')', '')
    detail = json.loads(html)
    return detail

def main():
    url='https://list.tmall.com/search_product.htm?spm=a220m.1000858.1000724.4.17ae2bea8wmi1M&q=%D0%D8%D5%D6&sort=d&style=g#J_Filter'
    get_rate(url)
    #print(get_html(url))


if __name__=='__main__':
    main()