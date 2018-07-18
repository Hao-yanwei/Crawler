from selenium import webdriver
import time

#创建一个浏览器客户端,并且指定配置
driver = webdriver.Chrome()

driver.get("https://www.douban.com/")
time.sleep(1)
driver.save_screenshot("豆瓣首页.png")

#输入账号
driver.find_element_by_id("form_email").send_keys("trygf521@126.com")
#输入密码
driver.find_element_by_name("form_password").send_keys("afu123456")
#保存验证码的图片
driver.save_screenshot("验证码.png")
#输入验证码
check_code = input("请输入验证码:")
print(r"验证码是多少:%s" % check_code)

driver.find_element_by_id("captcha_field").send_keys(check_code)

#点击登录按钮
driver.find_element_by_xpath("//input[@class='bn-submit']").click()

#休眠一下等待登录成功
time.sleep(3)
#保存登录成功的快照
driver.save_screenshot("登录成功.png")


#保存成功登录好的html到本地
with open("douban.html","w",encoding="utf-8") as f:
   f.write(driver.page_source)

#退出成功
driver.quit()

