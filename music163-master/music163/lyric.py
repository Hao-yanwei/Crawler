import requests
from bs4 import BeautifulSoup
import json
import re

url = 'http://music.163.com/api/song/lyric?id=514761281&lv=1&kv=1&tv=-1'
#      http://music.163.com/api/song/lyric?id=406232&lv=1&kv=1&tv=-1

lyrics = requests.get(url).text
print(lyrics)
print(">>>>>>>>>>>>>>>>")
lyric = json.loads(lyrics)
print(lyric)#打印出来j的类型是字典
print("=================")
try:  # 部分歌曲没有歌词，这里引入一个异常
    lrc = lyric['lrc']['lyric']
    pat = re.compile(r'\[.*\]')  # 下面这三行正则匹配删除时间轴
    lrc = re.sub(pat, "", lrc)
    lrc = lrc.strip()
    print(lrc)
except KeyError as e:
    pass
