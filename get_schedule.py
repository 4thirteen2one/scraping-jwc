#! /usr/bin/env python
# -*- coding:utf-8 -*-
# Name:爬取教务系统学生课表
# Version:0.1
# Author:4thirteen2one

import os
import sys
import re
import requests
from bs4 import BeautifulSoup
import getpass
# from prettytable import PrettyTable

s = requests.session()
    # 请求头
headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0"}

def sel_port():
    port = input('请选择查询端口（81端口/84端口）：')
    host = 'http://jwc.ctgu.edu.cn:{}/'.format(port)
    return host

def user_info():
    name = input('请输入您的学号：')
    password = getpass.getpass('请输入您的密码：')
    print('\n')
    return name,password

def aspx_id(url):
    "获取提交表单中要求的__VIEWSTATE和__EVENTVALIDATION"
    r = s.get(url)
    bs = BeautifulSoup(r.text.encode('utf-8'),'lxml')
    viewstate = bs.find('input',{'id':'__VIEWSTATE'})['value']
    eventvalidation = bs.find('input',{'id':'__EVENTVALIDATION'})['value']
    print('Update ASPX ID:{}'.format(r.status_code))
    return viewstate,eventvalidation

def get_captcha():
    "获取验证码，在本地打开并手动输入看到的验证码"
    captcha_url = 'jwc_glxt/ValidateCode.aspx'
    r = s.get(host+captcha_url,stream=True)
    # 验证码图片尺寸：60 * 25
    print('Get captcha: {}'.format(r.status_code))
    captcha = r.content
    # 保存验证码至当前文件夹
    try:
        with open('captcha.jpg','wb') as jpg:
            jpg.write(captcha)
    except IOError:
        print('IO Error\n')
    finally:
        jpg.close
    os.startfile('captcha.jpg')
    # 这里调用世界上最精密最先进的OCR设备——人的眼睛
    checkcode = input('Enter captcha：')
    return checkcode

def log_in():
    "提交用户名、密码和验证码，以及通过获取得到的表单其他项，登录教务系统"
    login_url = 'jwc_glxt/Login.aspx'
    # 登陆按钮图片尺寸：69*43
    viewstate,eventvalidation = aspx_id(host+login_url)
    login_info = {'__VIEWSTATE':viewstate,
                  '__EVENTVALIDATION':eventvalidation,
                  'txtUserName':name,
                  'txtPassword':password,
                  'CheckCode': checkcode,
                  'btnLogin.x':"57",
                  'btnLogin.y':"23",}
    r = s.post(host+login_url,data=login_info)
    print('Log in: {}'.format(r.status_code))

def sel_schedule():
    "选择想要查询的课表,返回网页代码"
    schedule_url = 'jwc_glxt/Course_Choice/Course_Schedule.aspx'
    viewstate,eventvalidation = aspx_id(host+schedule_url)

    status1 = False
    status2 = False
    counter = 0
    separating = '-' * 32 + '\n'
    while not(status1 and status2):
        print(separating)
        sel_year = input('请输入需要查询的学年：')
        sel_term = input('请输入需要查询的学期：')
        print(separating)
        status1 = 1996 <= int(sel_year) <= 2023
        status2 = 1 <= int(sel_term) <= 4
        if status1 and status2:
            print("输入有效！\n")
            break
        else:
            print("输入非法！请重新输入！")
        counter += 1
        if counter >= 3:
            print("你4不4傻？")

    select = {'__EVENTTARGET':'',
              '__EVENTARGUMENT':'',
              '__VIEWSTATE':viewstate,
              '__EVENTVALIDATION':eventvalidation,
              'ctl00$MainContentPlaceHolder$School_Year':sel_year,
              'ctl00$MainContentPlaceHolder$School_Term':sel_term,
              'ctl00$MainContentPlaceHolder$BtnSearch.x':'18',
              'ctl00$MainContentPlaceHolder$BtnSearch.y':'3'}
    r = s.post(host+schedule_url,data=select)
    print('Select schedule:{}\n'.format(r.status_code))
    return r

def get_schedule(page):
    "从当前页面获取课表,并将当前课表网页源码保存至本地"
    bs = BeautifulSoup(page.text.encode('utf-8'),'lxml')
    # bs4.BeautifulSoup
    table = bs.find('table',{'id':'ctl00_MainContentPlaceHolder_GridScore'})
    # bs4.element.Tag
    with open('table0.html','w+',encoding='utf-8') as f:
        f.write(str(table))
    try:
        print(table)
    except UnicodeEncodeError:
        print('显示不了！\n去特喵的巨硬!\n你，赶紧给劳资换MAC！\n')
    finally:
        print('你还不换用python3.6！\n')
    return table

def listify(table):
    "接受一段bs4.element.Tag对象的html表格代码，返回一个列表"
    schedule = []
    for tr in table.find_all('tr'):
        box = []
        for th in tr.find_all('th'):
            box.append(th.get_text())
        for td in tr.find_all('td'):
            box.append(td.get_text().replace(u'\xa0',u' '))
        schedule.append(box)
    return schedule

def query_course(schedule):
    "输入课程节次和日数，查询课程"
    print('查询课程：')
    quit0not = None
    status1 = False
    status2 = False
    separating = '-' * 32 + '\n'
    while not(status1 and status2) or (quit0not != 'y'):
        print(separating)
        day = int(input('周几啊？'))
        period = int(input('第几节（以大课为以一单位）：'))
        print(separating)
        status1 = 1 <= int(period) <= 6
        status2 = 1 <= int(day) <= 7
        if not(status1 and status2):
            print("输入非法！请重新输入！\n")
            continue
        course = schedule[period][day]
        print(course+'\n')
        quit0not = input('查询完毕？\n')

def log_out():
    "登出教务系统"
    global host,s
    logout_url = 'jwc_glxt/Login.aspx?xttc=1'
    xttc = s.get(host+logout_url)
    print('Log out: {}'.format(xttc.status_code))
    return xttc.status_code

if __name__ == '__main__':
    print('欢迎使用4thirteen2one的自制查询课表脚本！\n')
    # 选择端口
    host = sel_port()
    # 用户和密码
    name,password = user_info()
    # 验证码
    checkcode = get_captcha()
    # 登录
    log_in()
    # 选择课表查询
    sche_page = sel_schedule()
    # 从页面中提取课表
    table = get_schedule(sche_page)
    # 列表化课表
    schedule = listify(table)
    # 查询课程
    query_course(schedule)
    # 登出
    log_out()
