# -*- coding:utf-8 -*-

import requests
from lxml import etree


url = 'http://alpha.wallhaven.cc/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}
# 使用代理绕过防虫机制
try:
    html = requests.get(url, headers=headers)          # 获取网页源码
    # html = requests.get(url)
    selector = etree.HTML(html.text)          # 转换为XPath文件形式
    photourl = selector.xpath('//*[@id="featured"]/div/a')         # 以XPath方法获取目标，生成lxml.etree类的变量
except Exception as e:          # 如果源码读取失败或异常，则报错，并退出程序
    print "wallhaven code read failed, Report:" + str(e)          # 输出错误原因
    exit()          # 退出程序

photosurl = []        # 添加用于储存各个分网页的列表
for each in photourl:           # 按循环读取
    photosurl.append(each.attrib['href'])       # lmxl.etree元素的attrib(字典形式)存储了目标数据，将其读入分网页列表
# for each in photosurl:
#     print each
print "Photograph URLs detected."           # 确认已经读取各图片的URL地址

for i in range(0, len(photosurl)):           # 按顺序打开二级网页列表中的网页地址，i用于文件命名
    try:
        html = requests.get(photosurl[i])         # 获取二级网页源代码
        selector = etree.HTML(html.text)          # 转换为XPath形式
        photo = selector.xpath('//*[@id="wallpaper"]')        # 以XPath方法获取目标，此时photo为lmxl.etree的类的实例
        image = requests.get('http:'+str(photo[0].attrib['src']))         # 确定图片存储的url地址并读取内容
    except Exception as e:
        print "The No." + str(i) + " Photograph detected failed. Report:" + str(e)
    f = open('G:\mine\wall\wallpaper'+str(i)+'.jpg', 'wb')         # 输入存储位置，以二进制写入方式打开空白图片
    f.write(image.content)          # 写入图片内容
    f.close()           # 关闭文件，完成存储
    print "The No." + str(i) + " Photograph detected completed."

