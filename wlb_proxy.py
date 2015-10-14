# -*- coding:utf-8 -*-
__author__ = '双犬子'

import urllib
import urllib2
import re
import time
import chardet

print "Link Start!"
time_start = time.time()


urls = []
proxy = []
for i in range(1, 3):
    url = r"http://www.xicidaili.com/nn/"+str(i)
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    }
    req = urllib2.Request(url, headers=header)
    try:
        html = urllib2.urlopen(req)
        html_data = html.read()
        # print html_data
        # print html.info()
        html.close()
    except Exception as e:
        print str(e)
        html_data = ""

    proxy_search = r'<tr class="">.*?<td></td>.*?<td><img src=".*?" alt=".*?" /></td>.*?<td>(.*?)</td>\n      <td>(.*?)</td>.*?</td>'
    proxy += re.findall(proxy_search, html_data, re.S)

# proxy_dic_lis = []
# if proxy:
#     for each in proxy:
#         proxy_text = str(each[0]) + ":" + str(each[1])
#         proxy_lis = ["http:", proxy_text]
#         proxy_lis2 = []
#         proxy_lis2.append(proxy_lis)
#         proxy_dic = dict(proxy_lis2)
#         proxy_dic_lis.append(proxy_dic)
# else:
#     print "none"

# if proxy_dic_lis:
#     for each in proxy_dic_lis:
#         print each
# else:
#     print "None"

print ">proxy prepared."

proxy_list = []
url_test = "http://www.baidu.com"
if proxy:
    for each in proxy:
        req = urllib2.Request(url_test, headers=header)
        req.set_proxy(each[0], 'http')
        try:
            html = urllib2.urlopen(req, timeout=4)
            html_data = html.read()
            print str(each[0]) + " SUCCEED!"
            proxy_list.append(each)
            html.close()
        except Exception as e:
            print str(each[0]) + "\tfailed\t" + str(e)

if proxy_list:
    for each in proxy_list:
        print each
else:
    print "None"

print "Link Logout."
