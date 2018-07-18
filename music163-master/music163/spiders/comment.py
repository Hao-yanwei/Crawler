# -*- coding: utf-8 -*-
import scrapy
import re
import json
import requests
from scrapy import Spider, Request, FormRequest
from ..settings import DEFAULT_REQUEST_HEADERS
from ..items import MusicComments


class CommentSpider(scrapy.Spider):
    name = 'comment'
    allowed_domains = ['music.163.com']
    start_urls = ['http://music.163.com/']
    base_url = 'https://music.163.com'

    def start_requests(self):
        """周杰伦的url网址"""
        url = "https://music.163.com/artist/album?id=6452"
        yield Request(url, callback=self.parseMainPage)

    def parseMainPage(self, response):
        artist_albums = response.xpath(
            '//*[@class="u-page"]/a[@class="zpgi"]/@href').extract()  # 得到专辑页的翻页html elements列表
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
        # 此处为获取专辑的所有链接xpath语法
        albums = response.xpath('//*[@id="m-song-module"]/li/div/a[@class="msk"]/@href').extract()
        for album in albums:
            album_url = self.base_url + album
            # print("专辑url：",album_url)
            yield Request(album_url, callback=self.parse_album)

    # 此处通过歌曲专辑的url获取歌曲的链接
    def parse_album(self, response):
        # 此处为歌曲名的链接获取的xpath语法
        musics = response.xpath('//ul[@class="f-hide"]/li/a/@href').extract()
        # print("music链接地址：",musics)
        for music in musics:
            music_id = music[9:]
            music_url = self.base_url + music
            print("音乐链接:", music_url)
            yield Request(music_url, meta={'id': music_id}, callback=self.parse_music)

    def parse_music(self, response):
        music_id = response.meta['id']
        music = response.xpath('//div[@class="tit"]/em[@class="f-ff2"]/text()').extract_first()
        data = {
            'csrf_token': '',
            'params': 'wYgj45dlaQObdjJR7zAtdKnrN5Nk6v+ZYkb5tLkYgLDRutDdg7df7UhrnTgTdBYLYK6uzyUTK22lKJphsCR4qVk+gzpx2+PBfTYw5/cymP9sIuyVTruN2hd5QO0gydZLF9QCor31sTJp7JrTTBtMsmkfhk9v3pWJ5U2ntXVeAp9Q5CI7G4PtWqe2K43Z/xEaslmJXin1a/Rn73bgxpYDqF1Csjqk8gJ744Y+cQwi2i4=',
            'encSecKey': '8c365bd06e4c831dbdb8e44c0f6a25a0b1778459640357ea4fb9ec2d8ae8f521b66349b8d5f0d8bc96031414e551ad1938281e0f38b5eefc9b0aba5c95fb778a3cd03d00798d97fd7da7106db68326bbe2fa0445e505df10eb0660389a9c05bb07a42c3edefcd96ee678ce4408fc903f9a866272fa9a68bda771483d315088c7'
        }
        DEFAULT_REQUEST_HEADERS['Referer'] = self.base_url + '/playlist?id=' + str(music_id)
        music_comment = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_' + str(music_id)

        yield FormRequest(music_comment, meta={'id': music_id, 'song': music}, callback=self.parse_comment,
                          formdata=data)

    def parse_comment(self, response):
        result = json.loads(response.text)
        if 'hotComments' in result.keys():
            for comment in result.get('hotComments'):
                item = MusicComments()
                hotcomment_author = comment['user']['nickname']
                hotcomment = comment['content']
                hotcomment_like = comment['likedCount']
                hotcomment_avatar = comment['user']['avatarUrl']
                music_id = response.meta['id']
                music = response.meta['song']
                item['id'] = music_id
                item['song'] = music
                item['nickname'] = hotcomment_author
                item['avatarurl'] = hotcomment_avatar
                item['comments'] = hotcomment
                item['hotcomment_like'] = hotcomment_like
                print(">>>>>>>>>", music_id)
                print(">>>>>>>>>", music)
                print(">>>>>>>>>", hotcomment_author)
                print(">>>>>>>>>", hotcomment)
                print(">>>>>>>>>", hotcomment_like)
                print(">>>>>>>>>", hotcomment_avatar)
                for field in item.fields:
                    try:
                        item[field] = eval(field)
                    except:
                        print('Field is not defined', field)
                yield item
