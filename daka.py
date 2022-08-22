from os import spawnl
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from PIL import Image

import mxnet as mx
from cnocr import CnOcr
from cnocr.line_split import line_split
import re

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import smtplib
import email
# 负责构造文本
from email.mime.text import MIMEText
# 负责构造图片
from email.mime.image import MIMEImage
# 负责将多个对象集合起来
from email.mime.multipart import MIMEMultipart
from email.header import Header

import time

# SMTP服务器,这里使用qq邮箱
mail_host = "smtp.qq.com"
# 发件人邮箱
mail_sender = "###请将此处内容替换为发件人邮箱###"
# 邮箱授权码
mail_license = "###请将此处内容替换为授权码###"
# 收件人邮箱，可以为多个收件人
mail_receivers = ["###请将此处替换为收件人邮箱###"]
mm = MIMEMultipart('related')

ocr = CnOcr()

verdaka="True"

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("prefs", {"profile.password_manager_enabled": False, "credentials_enable_service": False})
while verdaka=="True":
    driver = webdriver.Chrome(executable_path= r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")


    driver.get('http://bdmobile.jxvtc.edu.cn/ReportServer?formlet=xxkj%2Fmobile%2Fbpa%2F%5B62a5%5D%5B5e73%5D%5B5b89%5D.frm&op=h5')
    username='###请输入学号或身份证###'    #输入账号
    password='###输入统一认证平台的密码###'    #输入密码
    a=True
    while a==True:
        inputElement = driver.find_element_by_id("username")
        inputElement.send_keys(username)
        inputElement = driver.find_element_by_id("password")
        inputElement.send_keys(password)
        #在网页文本框中 输入用户名密码
        driver.get_screenshot_as_file('screenshot.png')
        element = driver.find_element_by_id('veriyCodeImg')
        left = int(element.location['x'])-210
        top = int(element.location['y'])
        right = int(left + element.size['width']-20)
        bottom = int(element.location['y'] + element.size['height'])
        im = Image.open('screenshot.png')
        im = im.crop((left, top, right, bottom))
        im.save('code.png')
        # 截取网页获得验证码图像
        img_fp = 'code.png'
        img = mx.image.imread(img_fp, 1).asnumpy()
        line_imgs = line_split(img, blank=True)
        line_img_list = [line_img for line_img, _ in line_imgs]
        res = ocr.ocr_for_single_lines(line_img_list)
        ix=int(len(res[0]))
        verword=''
        if ix > 0:
            for letter in range(ix):
                verword=verword+str(res[0][letter])
            verword=re.sub('[^A-Za-z0-9]+', '', verword)    #去除除大小写字母数字之外的所有字符
        else:
            driver.refresh()
            continue
        inputElement = driver.find_element_by_id("veriyCode")
        inputElement.send_keys(verword)     #输入验证码
        print(verword)
        # 识别输入验证码
        button = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div/div/form/button")
        button.click()
        # 登录

        windows = driver.window_handles
        print(windows)
        vertext=''
        try:
            vertext=driver.find_element_by_id('msg').text
        except:
            msgx="False"
        else:
            msgx="True"
        #验证元素是否存在
        if msgx=="True":
            vertext=driver.find_element_by_id('msg').text
        print(vertext)
        if '验证码' in vertext:
            a=True
            driver.refresh()
        else:
            break
        #验证验证码是否通过，未通过则刷新页面重新填写
    print("2333333")
    time.sleep(10)
    windows = driver.window_handles
    print(windows)
    driver.current_window_handle
    driver.refresh()
    time.sleep(3)
    try:
        button = driver.find_element_by_xpath("/html/body/div/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div[1]/div/div[8]/div[1]/div/div/div[6]/div[1]/div/div/div/div/div[2]/div/div/span[1]")
    except:
        msgx="False"
    else:
        msgx="True"
    if msgx=="True":
        button = driver.find_element_by_xpath("/html/body/div/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div[1]/div/div[8]/div[1]/div/div/div[6]/div[1]/div/div/div/div/div[2]/div/div/span[1]")
        button.click()    #发热否
    else:
        continue
    # button = driver.find_element_by_xpath("/html/body/div/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div[1]/div/div[11]/div[1]/div/div/div[2]/div[1]/div/div/div/div/div[1]/div/div/span[1]")
    # button.click()    #是否经过风险区

    # button = driver.find_element_by_xpath("/html/body/div/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div[1]/div/div[12]/div[1]/div/div/div[2]/div[1]/div/div/div/div/div[5]/div/div/span[1]")
    # button.click()    #以上均无



    # element=driver.find_element_by_xpath("/html/body/div/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div[1]/div/div[11]/div[1]/div/div/div[4]")
    # meeting_div = element
    # element.click()
    # # js代码，修改属性值
    # js = "arguments[0].style = 'display:none;'"   #将遮挡元素设置为隐藏
    # driver.execute_script(js, meeting_div)     #执行js语句


    # time.sleep(3)
    # button = driver.find_element_by_xpath("/html/body/div/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div[1]/div/div[18]/div[1]/div/div/div[1]/div[1]/span")
    # button.click()    #点击提交

    try:
        button = driver.find_element_by_xpath("/html/body/div/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div[1]/div/div[18]/div[1]/div/div/div[1]/div[1]/span")
    except:
        msga="False"
    else:
        msga="True"
    if msga=="True":
        button = driver.find_element_by_xpath("/html/body/div/div/div/div/div/div/div/div/div[2]/div/div[1]/div/div[1]/div/div[18]/div[1]/div/div/div[1]/div[1]/span")
        button.click()    #发热否
    else:
        continue


    time.sleep(3)
    windows = driver.window_handles
    print(windows)
    try:
        driver.switch_to_window(windows[1])
    except:
        daka="False"
    else:
        daka="True"
    if daka=="True":
        driver.switch_to_window(windows[1])

    driver.get_screenshot_as_file('screenshot2.jpg')
    driver.quit()
    if daka == "False":
        verdaka="True"
    else:
        break


print("success")
time.sleep(3)



today=(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

subject_content = """打卡结果通知"""
# 设置发送者,注意严格遵守格式,里面邮箱为发件人邮箱
mm["From"] = "sender_name<打卡服务>"
# 设置接受者,注意严格遵守格式,里面邮箱为接受者邮箱
mm["To"] = "receiver_1_name<shield-tech@foxmail.com>"
# 设置邮件主题
mm["Subject"] = Header(subject_content,'utf-8')
# 邮件正文内容
body_content = """打卡成功""" + today
# 构造文本,参数1：正文内容，参数2：文本格式，参数3：编码方式
message_text = MIMEText(body_content,"plain","utf-8")
# 向MIMEMultipart对象中添加文本对象

image_file=open('screenshot2.jpg','rb')
image_data = image_file.read()
# 设置读取获取的二进制数据
message_image = MIMEImage(image_data)
message_image.add_header('Content-Disposition', 'attachment', filename='s.jpg')
# # 关闭刚才打开的文件
image_file.close()
# 添加图片文件到邮件信息当中去

mm.attach(message_image)

mm.attach(message_text)
# 创建SMTP对象
stp = smtplib.SMTP()
# 设置发件人邮箱的域名和端口，端口地址为25
stp.connect('smtp.qq.com', 25)  
# set_debuglevel(1)可以打印出和SMTP服务器交互的所有信息
stp.set_debuglevel(1)
# 登录邮箱，传递参数1：邮箱地址，参数2：邮箱授权码
stp.login(mail_sender,mail_license)
# 发送邮件，传递参数1：发件人邮箱地址，参数2：收件人邮箱地址，参数3：把邮件内容格式改为str
stp.sendmail(mail_sender, mail_receivers, mm.as_string())
print("邮件发送成功")
# 关闭SMTP对象
stp.quit()