
- 唯品会首页的女装图片，是一边滚动一边进行ajax异步加载的
- 这个靠常规的抓包实现起来很麻烦
- 使用selenium我们只需模拟用户多次下拉滚动条，一段时间之后再重新拿取渲染好的页面源码，就可以像爬取静态页面那样去爬取图片了
- 一边滚动一边加载
```
"""
创建无界面浏览器参数
"""

from selenium import webdriver
# 要想调用键盘按键操作需要引入keys包
from selenium.webdriver.common.keys import Keys
# 导入chrome选项
from selenium.webdriver.chrome.options import Options
# 创建chrome浏览器驱动，无头模式
import time
from bs4 import BeautifulSoup


chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_options)
 
```

