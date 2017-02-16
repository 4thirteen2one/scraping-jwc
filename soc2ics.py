#! /usr/bin/env python
# -*- coding:utf-8 -*-
# Name:爬取教务系统学生课表
# Version:0.1
# Author:4thirteen2one

import os
import sys
import re
import requests
from uuid import uuid1
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import getpass

separating = '-' * 32 + '\n'
s = requests.session()
# 请求头
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0"}


def sel_port():
    """选择端口"""
    port = input('请选择查询端口（81端口/84端口）：')
    jwc = 'http://jwc.ctgu.edu.cn:{}/'.format(port)
    return jwc


def user_info():
    """输入个人信息"""
    print(separating)
    input1 = input('请输入您的学号：')
    input2 = getpass.getpass('请输入您的密码：')
    print(separating)
    return input1, input2


def choose_term():
    """选择学年和学期"""
    status1 = False
    status2 = False
    counter = 0
    while not (status1 and status2):
        print(separating)
        cho_year = input('请输入需要查询的学年：')
        cho_term = input('请输入需要查询的学期：')
        print(separating)
        status1 = 1996 <= int(cho_year) <= 2023
        status2 = 1 <= int(cho_term) <= 4
        if status1 and status2:
            print("输入有效！")
            print(separating)
            break
        else:
            print("输入非法！请重新输入！")
        counter += 1
        if counter >= 3:
            print("你4不4傻？")
    return cho_year, cho_term


def aspx_id(url):
    """获取提交表单中要求的__VIEWSTATE和__EVENTVALIDATION"""
    r = s.get(url)
    bs = BeautifulSoup(r.text.encode('utf-8'), 'lxml')
    viewstate = bs.find('input', {'id': '__VIEWSTATE'})['value']
    eventvalidation = bs.find('input', {'id': '__EVENTVALIDATION'})['value']
    print('Update ASPX ID:{}'.format(r.status_code))
    return viewstate, eventvalidation


def get_captcha():
    """获取验证码，在本地打开并手动输入看到的验证码"""
    captcha_url = 'jwc_glxt/ValidateCode.aspx'
    r = s.get(host+captcha_url, stream=True)
    # 验证码图片尺寸：60 * 25
    print('Get captcha: {}'.format(r.status_code))
    captcha = r.content
    # 保存验证码至当前文件夹
    try:
        with open('captcha.jpg', 'wb') as jpg:
            jpg.write(captcha)
    except IOError:
        print('IO Error\n')
    os.startfile('captcha.jpg')
    # 这里调用世界上最精密最先进的OCR设备——人的眼睛
    got = input('Enter captcha：')
    return got


def log_in():
    """提交用户名、密码和验证码，以及通过获取得到的表单其他项，登录教务系统"""
    login_url = 'jwc_glxt/Login.aspx'
    # 登陆按钮图片尺寸：69*43
    viewstate, eventvalidation = aspx_id(host+login_url)
    login_info = {'__VIEWSTATE': viewstate,
                  '__EVENTVALIDATION': eventvalidation,
                  'txtUserName': name,
                  'txtPassword': password,
                  'CheckCode': checkcode,
                  'btnLogin.x': "57",
                  'btnLogin.y': "23"}
    r = s.post(host+login_url, data=login_info)
    print('Log in: {}'.format(r.status_code))


def courses_page(year, term):
    """打开课程查询页面，选择学期，返回所选学期课程页面"""
    schedule_url = 'jwc_glxt/Course_Choice/Stu_Course_Query.aspx'
    viewstate, eventvalidation = aspx_id(host+schedule_url)
    select = {'__EVENTTARGET': '',
              '__EVENTARGUMENT': '',
              '__VIEWSTATE': viewstate,
              '__EVENTVALIDATION': eventvalidation,
              'ctl00$MainContentPlaceHolder$School_Year': year,
              'ctl00$MainContentPlaceHolder$School_Term': term,
              'ctl00$MainContentPlaceHolder$BtnSearch.x': '18',
              'ctl00$MainContentPlaceHolder$BtnSearch.y': '3'}
    r = s.post(host+schedule_url, data=select)
    print('Choose schedule:{}'.format(r.status_code))
    return r


def get_table(page):
    """从当前页面获取课程列表,并将当前课表网页源码保存至本地"""
    bs = BeautifulSoup(page.text.encode('utf-8'), 'lxml')
    # bs4.BeautifulSoup
    table = bs.find('table', {'id': 'ctl00_MainContentPlaceHolder_GridCourse_Q'})
    # bs4.element.Tag
    with open('table0.html', 'w+', encoding='utf-8') as f:
        f.write(str(table))
    try:
        print(table)
    except UnicodeEncodeError:
        print('显示不了！\n去特喵的巨硬!\n赶紧给劳资换Mac！\n')
    finally:
        print('换Python3.6！')
        print(separating)
    return table


def get_courses(bs_tag):
    """接受一段bs4.element.Tag对象的html表格代码，返回一个列表"""
    whole = []
    for tr in bs_tag.find_all('tr'):
        # 每门课程的相关信息：课程编号、课程名称、课程学时、课程学分、上课教师、选课类型、上课时间
        tds = tr.find_all('td')
        # 过滤掉表头
        if tds:
            pass
        else:
            continue
        # td1：课程名称
        td1 = ' '.join(tds[1].get_text().split())
        # td4：上课老师
        td4 = ' '.join(re.compile(r'[\u4e00-\u9fa5]{2,3}').findall(tds[4].get_text()))
        # td6：上课时间及地点
        td6s = ' '.join(tds[6].get_text().replace(u'\xa0', u' ').split())
        # “起始周数 日期 节次 地点”的模板
        pattern = re.compile(
            r'(\d\d?-\d\d?[\u4e00-\u9fa5]\s[\u4e00-\u9fa5]{2}[1-7]\s\(\d\d?-\d\d?[\u4e00-\u9fa5]\)\s[A-Z]\d?-\d{3,4})')
        # 由模板匹配到的课程时间地点对组成的列表
        td6 = pattern.findall(td6s)
        # 如果是作业设计之类没有上课地点的课程，直接跳至下一课程的处理
        if td6:
            pass
        else:
            continue
        # 将每一时间地点对的课程按照“名称、老师、开始周数、结束周数、上课日期、节次、地点”的模板整理
        for i in td6:
            td6_n0 = int(re.compile(r'\d\d?').findall(i)[0])
            td6_n1 = int(re.compile(r'\d\d?').findall(i)[1])
            td6_n2 = int(re.compile(r'\d\d?').findall(i)[2])
            td6_n3 = (int(re.compile(r'\d\d?').findall(i)[3])+1)//2
            td6_t = re.compile(r'([A-Z]\d?-\d{3,4})').search(i).group()
            each = [td1, td4, td6_n0, td6_n1, td6_n2, td6_n3, td6_t]
            whole.append(each)
    return whole


def soc2ics(soc):
    """将课表信息写入.ics文件"""
    print('开始写入.ics文件……')
    print(separating)
    print('请设置开学第一周周一的日期：')
    stsy = int(input('年：'))
    stsm = int(input('月：'))
    stsd = int(input('日：'))
    term_start = datetime(stsy, stsm, stsd)
    today = datetime.now().strftime('%Y%m%d')
    present = datetime.now().strftime('%H%M%S')
    lesson_start = {1: '080000',
                    2: '100000',
                    3: '140000',
                    4: '160000',
                    5: '190000',
                    6: '210000'}
    lesson_end = {1: '094000',
                  2: '114000',
                  3: '154000',
                  4: '174000',
                  5: '204000',
                  6: '224000'}
    content_head = """
BEGIN:VCALENDAR
PRODID:-//CTGU//Schedule of Courses//CN
VERSION:2.0
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:Schedule of Courses
X-WR-TIMEZONE:Asia/Shanghai"""

    f = open('{}0{}.ics'.format(cho_year, cho_term), 'w+', encoding='utf-8')
    f.write(content_head)
    # 名称、老师、开始周数、结束周数、上课日期、节次、地点
    for course_info in soc:
        course_on = (term_start + timedelta(weeks=(course_info[2]-1),
                                            days=(course_info[4]-1))).strftime('%Y%m%d')
        deadline = (term_start + timedelta(weeks=(course_info[3]-1),
                                           days=(course_info[4]-1))).strftime('%Y%m%d')
        event = """
BEGIN:VEVENT
SUMMARY:{}
DTSTART;VALUE=DATE-TIME:{}T{}
DTEND;VALUE=DATE-TIME:{}T{}
DTSTAMP;VALUE=DATE-TIME:{}T{}Z
UID:{}
RRULE:FREQ=WEEKLY;COUNT={};INTERVAL=1
DESCRIPTION:{}
LOCATION:{}
END:VEVENT
""".format(course_info[0],
           course_on, lesson_start[course_info[5]],
           course_on, lesson_end[course_info[5]],
           today, present,
           str(uuid1())+'@CTGU',
           (course_info[3]-course_info[2]+1),
           course_info[1],
           course_info[6])
        f.write(event)
    content_root = """END:VCALENDAR"""
    f.write(content_root)
    f.close()
    print(separating)
    print('写入成功！\n请查看同级目录下的“{}0{}.ics”文件'.format(cho_year, cho_term))


def log_out():
    """登出教务系统"""
    logout_url = 'jwc_glxt/Login.aspx?xttc=1'
    xttc = s.get(host+logout_url)
    print('Log out: {}'.format(xttc.status_code))
    print(separating)
    return xttc.status_code


if __name__ == '__main__':
    print('欢迎使用4thirteen2one的自制查询课表脚本！\n')
    host = sel_port()
    name, password = user_info()
    checkcode = get_captcha()
    log_in()
    cho_year, cho_term = choose_term()
    sche_page = courses_page(cho_year, cho_term)
    log_out()
    table = get_table(sche_page)
    schedule = get_courses(table)
    soc2ics(schedule)
