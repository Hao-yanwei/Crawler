# -*- coding: utf-8 -*-
import scrapy
import re
import json
import requests
from scrapy import Spider, Request, FormRequest
from ..settings import DEFAULT_REQUEST_HEADERS
from ..items import Music163Item

class JiezhouSpider(scrapy.Spider):
    name = 'jiezhou'
    allowed_domains = ['music.163.com']
    start_urls = ['http://music.163.com/']
    base_url = 'https://music.163.com'

    def start_requests(self):
        """周杰伦的url网址"""
        url = "https://music.163.com/artist/album?id=6452"
        yield Request(url, callback=self.parseMainPage)

    """
    判断歌手专辑页面是否存在下一页
    得到专辑页的翻页html elements列表
    若为空，说明只有一页，即套用原parse_artist方法的代码，注意callback=self.parse_album
    若不为空，即该歌手专辑存在分页，那么得到分页的url，注意callback=self.parse_artist
    """
    def parseMainPage(self, response):
        artist_albums = response.xpath('//*[@class="u-page"]/a[@class="zpgi"]/@href').extract()  # 得到专辑页的翻页html elements列表
        if artist_albums == []:  # 若为空，说明只有一页，即套用原parse_artist方法的代码，注意callback=self.parse_album
            albums = response.xpath('//*[@id="m-song-module"]/li/div/a[@class="msk"]/@href').extract()
            for album in albums:
                album_url = self.base_url + album
                yield Request(album_url, callback=self.parse_album)
        else:  # 若不为空，即该歌手专辑存在分页，那么得到分页的url，注意callback=self.parse_artist
            for artist_album in artist_albums:
                artist_album_url = self.base_url + artist_album
                yield Request(artist_album_url, callback=self.parse_artist)

    # 获得所有歌手专辑的url
    def parse_artist(self, response):
        #此处为获取专辑的所有链接xpath语法
        albums = response.xpath('//*[@id="m-song-module"]/li/div/a[@class="msk"]/@href').extract()
        for album in albums:
            album_url = self.base_url + album
            # print("专辑url：",album_url)
            yield Request(album_url, callback=self.parse_album)

    #此处通过歌曲专辑的url获取歌曲的链接
    def parse_album(self, response):
        #此处为歌曲名的链接获取的xpath语法
        musics = response.xpath('//ul[@class="f-hide"]/li/a/@href').extract()
        # print("music链接地址：",musics)
        for music in musics:
            music_id = music[9:]
            music_url = self.base_url + music
            print("音乐链接:",music_url)
            yield Request(music_url, meta={'id': music_id}, callback=self.parse_music)


    # 获得音乐信息
    def parse_music(self, response):
        item = Music163Item()
        #获取歌曲id
        music_id = response.meta['id']
        music = response.xpath('//div[@class="tit"]/em[@class="f-ff2"]/text()').extract_first()
        #获取歌手
        artist = response.xpath('//div[@class="cnt"]/p[1]/span/a/text()').extract_first()
        #获取专辑
        album = response.xpath('//div[@class="cnt"]/p[2]/a/text()').extract_first()
        #歌词
        print('歌曲名称：',music)

        music_lyric = 'http://music.163.com/api/song/lyric?id=' + str(music_id) + "&lv=1&kv=1&tv=-1"
        print("歌词链接》》》》》》》",music_lyric)
        lyrics = requests.get(music_lyric).text
        lyric = json.loads(lyrics)
        print("=================")
        lrc = lyric['lrc']['lyric']
        pat = re.compile(r'\[.*\]')  # 下面这三行正则匹配删除时间轴
        lrc = re.sub(pat, "", lrc)
        lrc = lrc.strip()
        print(lrc)

        item['id'] = music_id
        item['music'] = music
        item['artist'] = artist
        item['album'] = album
        item['Lyric'] = lrc

        for field in item.fields:
            try:
                item[field] = eval(field)
            except:
                print('Field is not defined', field)
        yield item
