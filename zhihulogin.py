from selenium import webdriver
import time
import requests
import pytesseract
from PIL import Image
import base64
from selenium.webdriver.support.ui import WebDriverWait  # expected_conditions 类，负责条件出发
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By  # WebDriverWait 库，负责循环等待


def base64_to_image(base64iamge):
    # print("base64iamge==",base64iamge)
    base64iamge = base64iamge[len("data:image/jpg;base64,"):].replace("&#10;", "").replace("%0A", "")
    print(base64iamge)
    return base64iamge


def captcha(captcha_data):
    captcha_data = base64.b64decode(captcha_data)
    with open("captcha.jpg", "wb") as f:
        f.write(captcha_data)
    time.sleep(1)
    image = Image.open("captcha.jpg")
    try:
        code_text = pytesseract.image_to_string(image)
        print("机器识别的验证码是:", code_text)
    except Exception as e:
        print("机器识别出错了你===", e)

    comm = input("如果机器识别的验证码请安y,自己输入按其他键:")
    if comm == "Y" or comm == "y":
        return code_text
    else:
        text = input("请输入验证码：")
    # 返回用户输入的验证码
    return text


def zhihuLogin():
    # 构建一个Session对象，可以保存页面Cookie
    driver = webdriver.Chrome()

    driver.get("https://www.zhihu.com/signup?next=%2F")
    # 休眠一会等待数据
    time.sleep(1)
    driver.find_element_by_xpath('//div[@class="SignContainer-switch"]/span').click()
    # 保存快照
    driver.save_screenshot("知乎登录页面.png")
    time.sleep(1)

    driver.find_element_by_name("username").send_keys("trygf521@126.com")
    #
    driver.find_element_by_name("password").send_keys("afu123456")

    # 判断有没有验证码的元素节点

    if driver.page_source.find("Captcha-englishImg") != -1:  # 英文验证码
        print("英文验证码验证码出现了!..................")
        # time.sleep(5)
        try:
            # 页面一直循环，直到 id="myDynamicElement" 出现
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "Captcha-englishImg")))
        finally:
            print("英文等待结束")
        image_path = driver.find_element_by_xpath('//img[@class="Captcha-englishImg"]')
        image_path = image_path.get_attribute("src")
        print(image_path)
        if len(image_path) > len("data:image/jpg;base64,null"):
            image_data = base64_to_image(image_path)
            code_text = captcha(image_data)
            print("code_text==", code_text)
            # 1.得到图片路径后
            # 2.可以把图片下载下来
            # 3.放入到Tesseract识别处理成文字
            # 4.把文字输入到验证框
            # 5.点击登录按钮
            driver.find_element_by_name("captcha").send_keys(code_text)


    elif driver.page_source.find("Captcha-chineseImg") != -1:  # 中文验证码
        print("中文验证码验证码出现了!..................")
        try:
            # 页面一直循环，直到 id="myDynamicElement" 出现
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "Captcha-chineseImg")))
        finally:
            print("中文验证码等待结束")
        img = driver.find_element_by_xpath('//img[@class="Captcha-chineseImg"]')
        image_path = img.get_attribute("src")
        print(image_path)
        if len(image_path) > len("data:image/jpg;base64,null"):
            image_data = base64_to_image(image_path)
            code_text = captcha(image_data)
            print("code_text==", code_text)
        else:
            print("没有中文验证码..")

    else:
        print("没有验证码直接登录..................")
    # 点击登录
    driver.find_element_by_xpath('//div[@class="Login-content"]/form/button').click()
    time.sleep(2)

    # 保存快照
    driver.save_screenshot("登录成功.png")
    time.sleep(1)

    driver.quit()
    # time.sleep(10000)


if __name__ == "__main__":
    zhihuLogin()
