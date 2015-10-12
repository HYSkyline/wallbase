# -*- coding:utf-8 -*-
import re
import requests
from time import sleep
# tag_time=time.strftime("%m%d%H%M%S",time.localtime(time.time()))          #确定当前时间
# num=input('how many pages do you want to check?')           #确定要读取的最大页数
num=2
for each in range(1,num+1):          #按页码开始循环
    init_url='http://alpha.wallhaven.cc/random?page='+str(each)            #根据页码确定主网页地址
    html=requests.get(init_url)         #读取主网页源代码
    photourls=re.findall('title="Tags" href="(.*?)" ><i class="fa fa-fw fa-tags">',html.text,re.S)          #以正则表达式读取分网页地址
    #分网页地址的列表中各项开头均带有u，可以忽略直接执行程序
    for i in range(0,len(photourls)):           #按每一页的分网页开始循环
        url=photourls[i]            #从分网页地址列表中读取目标分网页地址
        sleep(5)            #静默5秒，防止网站服务器因访问流量过大关闭连接
        html=requests.get(url)          #读取分网页源代码
        photos=re.findall('<img id="wallpaper" src="(.*?)" alt="',html.text,re.S)           #以正则表达式确定图片文件的具体存储位置

        image=requests.get('http:'+photos[0])           #读取图片内容，此时photos字符串中也以u开头，但不影响程序执行

        f=open(r'G:\mine\wall\img'+str(each)+'_'+str(i)+'.jpg','wb')           #将图片存储至相应目录当中，以r开头规避\t影响
        f.write(image.content)          #写入图片内容
        f.close()           #关闭文件