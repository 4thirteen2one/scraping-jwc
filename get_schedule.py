#! /usr/bin/env python
# -*- coding:utf-8 -*-
import os,sys,re
import requests
from bs4 import BeautifulSoup
import getpass
# from prettytable import PrettyTable

def get_sessionID(url):
    global s
    r = s.get(url)
    print('Get session: {}'.format(r.status_code))
    sessionID = r.headers['Set-Cookie'].split(';')[0].split('=')[1]
    return sessionID

def sheet_req(url):
    '''
    <input type="hidden" 
           name="__VIEWSTATE" 
           id="__VIEWSTATE" 
           value="/wEPDwUKMTQ4NjM5NDA3OWQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFCGJ0bkxvZ2luU077LK9itKNe3fhI7aoZZ+S5Ryo=" />
    <input type="hidden" 
           name="__EVENTVALIDATION" 
           id="__EVENTVALIDATION" 
           value="/wEWBQKOmrqLAwKl1bKzCQKC3IeGDAK1qbSRCwLO44u1DVzfq830wXTY29pyqB1kTMdgWLfG" />
    '''
    global s
    r = s.get(url)
    print('Get sheet_req:{}'.format(r.status_code))
    bs = BeautifulSoup(r.text,'lxml')
    viewstate = bs.find('input',{'id':'__VIEWSTATE'})['value']
    eventvalidation = bs.find('input',{'id':'__EVENTVALIDATION'})['value']
    return (viewstate,eventvalidation)

def get_captcha(url):
    '''
    <img title="不区分大小写!红色数字,黑色字母!" 
         id="ImageCheck" 
         style="border-width:0px;" 
         src="ValidateCode.aspx">
    '''
    # 验证码图片尺寸：60 * 25
    global s
    r = s.get(url,stream=True)
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
    checkcode = input('Enter the captcha：')
    return checkcode

def log_in(url):
    global s
    login_info = {'__VIEWSTATE': viewstate,
                  '__EVENTVALIDATION': eventvalidation,
                  'txtUserName': str(name),
                  'txtPassword':str(password),
                  'btnLogin.x':"57", 'btnLogin.y':"23",
                  'CheckCode':checkcode}
    r = s.post(host+login_url,data=login_info)
    print('Log in: {}'.format(r.status_code))

def get_schedule(url):
    '''
    <table class="GridViewStyle" 
           rules="all" 
           id="ctl00_MainContentPlaceHolder_GridScore" 
           style="border-collapse:collapse;" 
           cellspacing="0" border="1">
    '''
    global s
    init = s.get(url)
    bs = BeautifulSoup(init.content.decode('utf-8'),'lxml')
    table0 = bs.find('table',{'id':'ctl00_MainContentPlaceHolder_GridScore'})
    schedule = []
    for child in table0.children:
        box = []
        for i in child:
            diff = []
            if hasattr(i,'get_text'):
                pattern = r'[\u4e00-\u9fa5]+ [A-Z]-\d{3,4}\s\d\d-\d\d?[\u4e00-\u9fa5]\s[\u4e00-\u9fa5]+''
                if re.match(pattern,i.get_text()):
                    pass
                box.append(i.get_text().replace(u'\xa0',u' '))
        schedule.append(box)
    with open('table.txt','w+',encoding='utf-8') as saveit:
        for box in schedule:
            for i in box:
                saveit.write(i)

    '''
    sel_year = int(input('请输入需要查询的学年：'))
    sel_term = int(input('请输入需要查询的学期：'))
    select = {'__EVENTTARGET':'',
              '__EVENTARGUMENT':'',
              '__VIEWSTATE':viewstate,
              '__EVENTVALIDATION':eventvalidation,
              'ctl00$MainContentPlaceHolder$School_Year':sel_year,
              'ctl00$MainContentPlaceHolder$School_Term':sel_term,
              'ctl00$MainContentPlaceHolder$BtnSearch.x':'18',
              'ctl00$MainContentPlaceHolder$BtnSearch.y':'3'}
    
    r = s.post(url,data=select)
    print('Get schedule:{}'.format(r.status_code))
    bs = BeautifulSoup(r.text,'lxml')
    table1 = bs.find('table',{'id':'ctl00_MainContentPlaceHolder_GridScore'})
    for child in table1.children:
        print(child)
    print(len(table1))'''

def log_out(url):
    global s
    xttc = s.get(url)
    print('Log out: {}'.format(xttc.status_code))

if __name__ == '__main__':
    print('欢迎使用闵冲的自制查询课表脚本！')
    port = input('请选择查询端口：81端口 or 84端口？')
    name = input('请输入您的学号：')
    password = getpass.getpass('请输入您的密码：')

    host = 'http://jwc.ctgu.edu.cn:{}/'.format(port)
    login_url = 'jwc_glxt/Login.aspx'
    logout_url = 'jwc_glxt/Login.aspx?xttc=1'
    captcha_url = 'jwc_glxt/ValidateCode.aspx'
    schedule_url = 'jwc_glxt/Course_Choice/Course_Schedule.aspx'
    s = requests.session()
    
    sessionID = get_sessionID(host+login_url)
    checkcode = get_captcha(host+captcha_url)
    viewstate,eventvalidation = sheet_req(host+login_url)

    headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0"}
    cookies = {'ASP.NET_SessionId':get_sessionID,
               '_gscu_891807511':''}

    # 登陆按钮图片尺寸：69*43
    log_in(host+login_url)
    get_schedule(host+schedule_url)
    log_out(host+logout_url)
    '''
    选修课表：http://jwc.ctgu.edu.cn:81/jwc_glxt/Course_Choice/Course_Schedule.aspx
    id="ct100_Menu1n9"
    主课表：id="ctl00_MainContentPlaceHolder_GridScore"
    作业设计：id="ctl00_MainContentPlaceHolder_Label1"
    选择学年：id="ctl00_MainContentPlaceHolder_School_Year"
    选择学期：id="ctl00_MainContentPlaceHolder_School_Term"
    搜索：id="ctl00_MainContentPlaceHolder_BtnSearch"
    '''