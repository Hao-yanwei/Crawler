
--------------------
##### 1. Cookie 介绍


HTTP 协议是无状态的。因此，若不借助其他手段，远程的服务器就无法知道以前和客户端做了哪些通信。Cookie 就是「其他手段」之一。 Cookie 一个典型的应用场景，就是用于记录用户在网站上的登录状态。

- 1.用户登录成功后，服务器下发一个（通常是加密了的）Cookie 文件。
- 2.客户端（通常是网页浏览器）将收到的 Cookie 文件保存起来。
- 3.下次客户端与服务器连接时，将 Cookie 文件发送给服务器，由服务器校验其含义，恢复登录状态（从而避免再次登录）。
##### 2. requests使用cookie
当浏览器作为客户端与远端服务器连接时，远端服务器会根据需要，产生一个 `SessionID`，并附在 Cookie 中发给浏览器。接下来的时间里，只要 `Cookie` 不过期，浏览器与远端服务器的连接，都会使用这个 `SessionID`；而浏览器会自动与服务器协作，维护相应的 `Cookie`。
在 `requests 中`，也是这样。我们可以创建一`requests.Session`，尔后在该 `Session` 中与远端服务器通信，其中产生的 `Cookie`，`requests` 会自动为我们维护好。
##### 3. POST 表单
post 方法可以将一组用户数据，以表单的形式发送到远端服务器。远端服务器接受后，依照表单内容做相应的动作。
调用 `requests` 的 POST 方法时，可以用 data 参数接收一个 Python 字典结构。requests 会自动将 Python 字典序列化为实际的表单内容。
##### 4. 实际模拟登录 GitHub 试试看
在 Chrome 的审查元素窗口中，我们可以看到提交给 session 接口的表单信息。
![1.png](https://upload-images.jianshu.io/upload_images/6591571-4e04aa972fd7e56b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

其中，`commit `和 `utf8` 两项是定值；`login `和 `password` 分别是用户名和密码，这很好理解。唯独 `authenticity_token` 是一长串无规律的字符，我们不清楚它是什么。
POST 动作发生在与 session 接口交互之前，因此可能的信息来源只有 login 接口。我们打开 login 页面的源码，试着搜索 authenticity_token 就不难发现有如下内容：
```
<input name="authenticity_token" type="hidden" value="......" />
```
原来，所谓的 authenticity_token 是明白写在 HTML 页面里的，只不过用 hidden 模式隐藏起来了。为此，我们只需要使用 Python 的正则库解析一下，就好了。
```
import requests
from lxml import etree


class Login(object):
    def __init__(self):
        # 模拟浏览器的请求头
        self.headers = {
            'Referer': 'https://github.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Host': 'github.com'
        }
        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/session'
        self.session = requests.Session()


    def token(self):
        response = self.session.get(self.login_url, headers=self.headers)
        selector = etree.HTML(response.text)
        token = selector.xpath('//div//input[2]/@value')
        print(token)
        return token

    def login(self, email, password):
        """
        在github点击登陆按钮时，在 Chrome 的审查元素窗口中，我们可以看到提交给 session 接口的表单信息
        注意（post_data的内容要和from_date的信息完全一致，
        其中authenticity_token的内容为我们在h5页面中提交时，type='hidden'的内容）
        """
        post_data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.token()[0],
            'login': email,
            'password': password
        }
        response = self.session.post(self.post_url, data=post_data, headers=self.headers)
        if response.status_code == 200:
            self.dynamics(response.text)
            # print(response.text)

    def dynamics(self, html):
        selector = etree.HTML(html)
        dynamics = selector.xpath('//div[contains(@class, "news")]//div[contains(@class, "alert")]')
        for item in dynamics:
            dynamic = ' '.join(item.xpath('.//div[@class="title"]//text()')).strip()
            print(dynamic)


if __name__ == "__main__":
    login = Login()
    login.login(email='username', password='pwd')#此处填写你的用户名和密码
```

> 1. 首先，我们准备好了和 Chrome 一致的 HTTP 请求头部信息。具体来说，其中的 User-Agent 是比较重要的。
> 2. 仿照浏览器与服务器的通信，我们创建了一个 requests.Session。
>  3. 我们用 GET 方法打开登录页面，并用正则库解析到 authenticity_token。
> 4. 将所需的数据，整备成一个 Python 字典login_data
> 5. 最后，用 POST 方法，将表单提交到 session 接口。
>  6. 最终的结果经由 302 跳转，打开了（200）GitHub 首页.

