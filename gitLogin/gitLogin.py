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