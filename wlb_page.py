# -*- coding:utf-8 -*-
import re
import requests
import time

print "Link Start!"
t1 = time.time()

# tag_time=time.strftime("%m%d%H%M%S",time.localtime(time.time()))          # 确定当前时间
num = input('how many pages do you want to check?')           # 确定要读取的最大页数
urlpage_list = []
url_list = []
for each in range(1, num+1):          # 按页码开始循环
    init_url = 'http://alpha.wallhaven.cc/random?page='+str(each)            # 根据页码确定主网页地址
    html = requests.get(init_url)         # 读取主网页源代码
    urlpage_list.append(re.findall('title="Tags" href="(.*?)" ><i class="fa fa-fw fa-tags">', html.text, re.S))          # 以正则表达式读取分网页地址
    print u'第' + str(each) + u'页分析完成.'
# 分网页地址的列表中各项开头均带有u，可以忽略直接执行程序
for each in urlpage_list:
    for eachone in each:
        url_list.append(eachone)
print u'图片网页地址分析完成.总计' + str(len(url_list)) + u'个目标.'

error_list = []
for i in range(0, len(url_list)):           # 按每一页的分网页开始循环
    url = url_list[i]            # 从分网页地址列表中读取目标分网页地址
    html = requests.get(url)          # 读取分网页源代码
    photos = re.findall('<img id="wallpaper" src="(.*?)" alt="',html.text,re.S)           # 以正则表达式确定图片文件的具体存储位置
    try:
        image = requests.get('http:'+photos[0])           # 读取图片内容，此时photos字符串中也以u开头，但不影响程序执行
        f = open(r'G:\mine\wall\img' + str(i+1) + '.jpg', 'wb')           # 将图片存储至相应目录当中，以r开头规避\t影响
        f.write(image.content)          # 写入图片内容
        f.close()           # 关闭文件
        print u"第" + str(i+1) + u"张图片读取完成,任务进度(" + str(i+1) + u'/' + str(len(url_list)) + u")"
    except Exception as e:
        print u"第" + str(i+1)+ u"张图片读取失败,错误来自于" + str(e)
        error_list.append(str(i+1))

t2 = time.time()
time_cost = t2 - t1
print "Link Report:"
print "Time used:" + str(time_cost) + 'seconds.'
print str(len(url_list)-len(error_list)) + '/' + str(len(url_list)) + 'completed.'
sep = "、"
if len(error_list) == 0:
    print 'No.' + sep.join(error_list) + " photo failed."
else:
    print 'All photos read.'
print "Link Logout."
