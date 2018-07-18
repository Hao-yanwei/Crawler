-----------------
#### 一、机器视觉与Tesseract介绍
###### 1\. 机器视觉

从 Google 的**无人驾驶汽车**到可以**识别假钞**的自动售卖机，机器视觉一直都是一个应用广 泛且具有深远的影响和雄伟的愿景的领域。

我们将重点介绍机器视觉的一个分支：**文字识别**，介绍如何用一些 Python库来识别和使用在线图片中的文字。

**我们可以很轻松的阅读图片里的文字，但是机器阅读这些图片就会非常困难，利用这种人类用户可以正常读取但是大多数机器人都没法读取的图片，验证码 (CAPTCHA)****就出现了**。验证码读取的难易程度也大不相同，有些验证码比其他的更加难读。

将图像翻译成文字一般被称为**光学文字识别****(**Optical Character Recognition, OCR)。可以实现OCR的底层库并不多,目前很多库都是使用共同的几个底层 OCR 库,或者是在上面 进行定制。

###### 2\. ORC库概述

在读取和处理图像、图像相关的机器学习以及创建图像等任务中，Python 一直都是非常出色的语言。虽然有很多库可以进行图像处理，但在这里我们只重点介绍：[Tesseract](https://pypi.python.org/pypi/pytesseract)

###### Tesseract

Tesseract 是一个 OCR 库,目前由 Google 赞助(Google 也是一家以 OCR 和机器学习技术闻名于世的公司)。T**esseract** **是目前公认最优秀、最精确的开源 OCR 系统**。  除了极高的精确度,Tesseract 也具有很高的灵活性。它可以通过训练识别出任何字体，也可以识别出任何 Unicode 字符。

###### 3. 安装Tesseract
###### 3.1 Linux 系统
安装 tesseract-ocr     可以通过 apt-get 安装:命令：`sudo apt-get install tesseract-ocr`
`Tesseract-OCR`引擎，注意要3.0以上才支持中文
安装参考：http://www.cnblogs.com/dajianshi/p/4932882.html
###### 3.2 Windows 系统

下载可执行安装文件[https://code.google.com/p/tesseract-ocr/downloads/list](https://code.google.com/p/tesseract-ocr/downloads/list)安装。
百度经验：https://jingyan.baidu.com/article/219f4bf788addfde442d38fe.html

在 Windows 系统上也类似,你可以通过下面这行命令设置环境变量: `#setx TESSDATA_PREFIX C:\Program Files\Tesseract OCR\Tesseract`

参考帖子：[http://blog.csdn.net/wenhao_ir/article/details/52213224](http://blog.csdn.net/wenhao_ir/article/details/52213224)
######4. 安装pytesseract
`Tesseract` 是一个 Python 的命令行工具，不是通过 import 语句导入的库。安装之后,要用 tesseract 命令在 Python 的外面运行，也就是在Linux命令环境执行，但我们可以通过 pip 安装支持Python 版本的 Tesseract库，就可以支持在python内页可以使用Tesseract库了：
Python3安装命令：`sudo pip3 install pytesseract`

###### 5. 通过Python代码实现
```
# tesseract是google维护的具有学习功能的OCR引擎，3.0以后支持中文识别
import pytesseract
# Python Imaging Library，已经是Python平台事实上的图像处理标准库了。
# PIL功能非常强大，但API却非常简单易用
from PIL import Image

# 使用PIL的Image.open()函数加载图片
image = Image.open("3.png")
# print(image)

# 使用 pytesseract 模块的image_to_string把图片识别成文字
text = pytesseract.image_to_string(image)
# 打印文本
print(text)

```
![example.png](https://upload-images.jianshu.io/upload_images/6591571-9f9aea32bc446ee0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![Image 1.png](https://upload-images.jianshu.io/upload_images/6591571-a575444631bf8a6c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)






