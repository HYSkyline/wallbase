# -*- coding:utf-8 -*-
import re
import requests
import time
import threading


def main0():
    print "Link Start!"         # 开始连接！
    t0 = time.time()            # 确定当前系统时间,用于程序运行时长计算
    page_num = input('Page number?\n')          # 确定要读取的页数数量

    # thread_num = input('Thread number?\n')
    # url_list = page_url(page_num, thread_num)           # 通过page_url函数读取每页中图片的URL地址（一级页面）
    # error_list = thread_test(url_list)          # 通过thread_test函数进行图片读取，并输出报错信息

    return_list = detect(page_num)            # 通过detect函数读取图片，并输出每页中图片的URL地址与具体读取过程中的报错信息
    url_list = return_list[0]         # 对detect函数返回的result_list进行解译
    error_list = return_list[1]

    report(t0, url_list, error_list)            # 输出报告

    print "Link Logout."            # 连接结束


def main1():
    print "Link Start!"         # 开始连接！
    print ''
    t0 = time.time()            # 确定当前系统时间,用于程序运行时长计算
    page_num = input('Page number?\n')          # 确定要读取的页数数量

    thread_num = input('Thread number?\n')
    url_list = page_url(page_num)           # 通过page_url函数读取每页中图片的URL地址（一级页面）
    error_list = thread_test(url_list, thread_num)          # 通过thread_test函数进行图片读取，并输出报错信息

    # return_list = detect(page_num)            # 通过detect函数读取图片，并输出每页中图片的URL地址与具体读取过程中的报错信息
    # url_list = return_list[0]         # 对detect函数返回的result_list进行解译
    # error_list = return_list[1]

    report(t0, url_list, error_list)            # 输出报告

    print "Link Logout."            # 连接结束


def thread_test(url_list, thread_num):
    threadpool = []         # 创建进程池
    errors = []         # 准备搜集报错信息
    error_list = []         # 准备报错信息的输出列表（在搜集报错时会产生元素为None但长度不为0的列表）
    targets_total_num = len(url_list)           # 计算总目标数
    targets_each_missionnum = targets_total_num / thread_num         # 默认为8个线程，所有任务按序号进行8等分，分配到每个线程中去
    url_distribution = []           # 准备每个线程的任务列表
    for i in range(0, thread_num):           # 默认为8个线程
        url_distribution.append(thread_mission_distribution(url_list, targets_each_missionnum, i))          # 对任务进行等分
    threadcode = 0          # 线程代码
    for each in url_distribution:           # 按照每个线程的任务进行循环，准备向线程中输入任务
        threadcode += 1
        th = threading.Thread(target=photo_catch, args=(each, threadcode))         # 创建含有任务的线程
        threadpool.append(th)           # 将线程填入线程池
    for th in threadpool:
        errors.append(th.start())           # 线程池中的每个线程开始工作，并以errors列表收集每个线程的报错信息
    for th in threadpool:
        threading.Thread.join(th)           # 所有线程全部结束后才开始进行主线程
    print "All threads completed."         # 报告分线程结束
    for each in errors:         # 如果errors内均为None变量，则error_list应为长度为0的空列表
        if each is None:
            pass
        else:
            error_list.append(each)
    return error_list           # 输出error_list


def thread_mission_distribution(url_list, num, i):
    url_distribution_list = []          # 准备单个线程的任务分配列表
    for ii in range(0, num):
        url_distribution_list.append(url_list[i * num + ii])          # 按照任务分配个数与当前序号对任务进行等分，选择此线程应执行的任务
    return url_distribution_list            # 返回此线程的任务分配列表


def detect(page_num):
    return_list = []            # 准备用于输出的结果列表
    url_list = page_url(page_num)           # 以page_url函数确定所有页面上全部图片的URL（一级页面）
    error_list = photo_catch(url_list, 0)           # 以photo_catch函数进行图片读取，并返回报错信息
    return_list.append(url_list)            # 将图片URL列表与报错信息列表封装入单个列表（result_list）用于输出
    return_list.append(error_list)
    return return_list          # 输出结果列表


def page_url(num):
    url1_list = []           # 准备每个图片网页URL的列表
    for each in range(1, num + 1):          # 按页码开始循环
        init_url = 'http://alpha.wallhaven.cc/random?page='+str(each)            # 根据页码确定主网页地址
        html = requests.get(init_url)         # 读取主网页源代码
        url_list = re.findall('title="Tags" href="(.*?)" ><i class="fa fa-fw fa-tags">', html.text, re.S)          # 读取分网页地址
        for eachone in url_list:            # 此处url_list第一级编号为页数，第二级编号才是图片序号
            url1_list.append(eachone)           # 略去页数信息
        print 'No.' + str(each) + ' page analysed.'          # 报告当前页所有图片URL读取完成
        # 分网页地址的列表中各项开头均带有u，可以忽略直接执行程序
    print 'All photourls analysed.Totally ' + str(len(url1_list)) + ' targets.'          # 报告所有页全部图片URL读取完成
    return url1_list            # 输出全部图片URL列表（一级页面）


def photo_catch(url_list, threadcode):
    error_list = []         # 准备输出报错信息列表
    for i in range(0, len(url_list)):           # 按每一页的分网页开始循环
        url = url_list[i]            # 从分网页地址列表中读取目标分网页地址
        html = requests.get(url)          # 读取分网页源代码
        photos = re.findall('<img id="wallpaper" src="(.*?)" alt="', html.text, re.S)           # 确定图片文件的具体存储位置（二级页面）
        try:
            image = requests.get('http:'+photos[0])           # 读取图片内容，此时photos字符串中也以u开头，但不影响程序执行
            photo_save(i, image, threadcode)            # 以photo_save函数保存图片
            print "from thread " + str(threadcode) + ":No." + str(i+1) + " target detected, process:(" + str(i+1) + '/' + str(len(url_list)) + ")"         # 报告图片读取信息
        except Exception as e:
            print "No." + str(i+1) + " t failed, error:" + str(e)           # 报告图片读取失败并输出报错信息
            error_list.append(str(i+1))         # 报错信息填入报错列表
    return error_list           # 输出报错信息列表


def photo_save(i, image, threadcode):
    f = open(r'D:\ctemp\wall\img' + str(threadcode) + '-' + str(i+1) + '.jpg', 'wb')           # 将图片存储至相应目录当中，以r开头规避\t影响
    f.write(image.content)          # 写入图片内容
    f.close()           # 关闭文件


def report(t1, url_list, error_list):
    t2 = time.time()            # 获取图片读取完成时的系统时间
    time_cost = t2 - t1         # 计算图片读取过程时长
    print ''
    print "Link Report:"
    print "Time used:%.3f" % float(time_cost) + 's'          # 报告时长信息
    print str(len(url_list)-len(error_list)) + '/' + str(len(url_list)) + 'completed.'          # 报告图片读取完成与报错信息
    sep = "、"
    if len(error_list) != 0:            # 如果存在图片读取失败
        print 'No.' + sep.join(error_list) + " target failed."
    else:
        print 'All targets completed.'
    print ''


if __name__ == '__main__':
    mode = input('Single thread(0)/Multiple threads(1)?\nplease enter 0 or 1\n')
    if mode == 0:
        main0()
    elif mode == 1:
        main1()
    else:
        print 'Unknow mode.'
        exit()
