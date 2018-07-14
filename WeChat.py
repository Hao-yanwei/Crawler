import os
import time
filename = "E:/171125/爬虫/Headportrait/"
#coding=utf8
import  itchat
itchat.auto_login(hotReload=True)   #热启动你的微信

room = itchat.search_friends(name=r'王明阳')  #这里输入你好友的名字或备注。
print(room)
userName = room[0]['UserName']
# f="C:\文件/lh.jpg"  #图片地址
g = os.walk(filename)
for path,d,filelist in g:
    for filename in filelist:
        if filename.endswith('jpg')or filename.endswith('gif'):
            jpg = os.path.join(path, filename)
            print(jpg)

            try:
                itchat.send_image(jpg,toUserName=userName)
                time.sleep(0.5)
                # 如果是其他文件可以直接send_file
                print("success")
            except:
                print("fail")