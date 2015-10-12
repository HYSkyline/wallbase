# -*- coding:utf-8 -*-

import requests
from lxml import etree


url='http://alpha.wallhaven.cc/'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}
#使用代理绕过防虫机制
html=requests.get(url,headers=headers)          #获取网页源码
# html=requests.get(url)
selector=etree.HTML(html.text)          #转换为XPath文件形式
photourl=selector.xpath('//*[@id="featured"]/div/a')         #以XPath方法获取目标，生成lxml.etree类的变量
photosurl=[]        #添加用于储存各个分网页的列表

# print type(photourl[0])           #确定变量类型
# print dir(photourl[0])            #确定变量存在的属性与方法
for each in photourl:           #按循环读取
    photosurl.append(each.attrib['href'])       #lmxl.etree元素的attrib(字典形式)存储了目标数据，将其读入分网页列表


for i in range(0,len(photosurl)):           #按顺序打开分网页列表中的网页地址，i用于文件命名
    html=requests.get(photosurl[i])         #获取分网页源代码
    selector=etree.HTML(html.text)          #转换为XPath形式
    photo=selector.xpath('//*[@id="wallpaper"]')        #以XPath方法获取目标，此时photo为lmxl.etree的类的实例

    image=requests.get('http:'+str(photo[0].attrib['src']))         #确定图片存储的url地址并读取内容

    f=open('G:\mine\wall\wallpaper'+str(i)+'.jpg','wb')         #打开空白图片
    f.write(image.content)          #写入图片内容
    f.close()           #关闭文件

