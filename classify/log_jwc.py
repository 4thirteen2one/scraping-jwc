#! /usr/bin/env python
# -*- coding:utf-8 -*-
# Name:爬取教务系统学生课表
# Version:0.1
# Author:4thirteen2one

import requests

s = requests.session()

def sel_port():
    """选择端口"""
    print('\t[81：81端口]  [84：84端口]\n')
    port = input('\t请选择查询端口：')
    while True:
        if port in ['81','84']:
            break
        else:
            port  = input('\n\t请重新选择端口:')
    host = 'http://jwc.ctgu.edu.cn:{}/'.format(port)
    return host

def user_info():
    """输入个人信息"""
    username = input('\t请输入您的学号：')
    password = getpass.getpass('\n\t请输入您的密码：')
    return username, password

def get_captcha():
    """获取验证码，在本地打开并手动输入看到的验证码"""
    captcha_url = 'jwc_glxt/ValidateCode.aspx'
    r = s.get(host+captcha_url, stream=True)
    # 验证码图片尺寸：60 * 25
    # 保存验证码至当前文件夹
    try:
        with open('captcha.jpg', 'wb') as jpg:
            jpg.write(r.content)
    except IOError:
        print('IO Error\n')
    os.startfile('captcha.jpg')
    # 这里调用世界上最精密最先进的OCR设备——人的眼睛
    captcha = input('\t输入验证码：')
    return captcha

def get_aspxID(url):
    """获取提交表单中要求的__VIEWSTATE和__EVENTVALIDATION"""
    r = s.get(url)
    bs = BeautifulSoup(r.text.encode('utf-8'), 'lxml')
    viewstate = bs.find('input', {'id': '__VIEWSTATE'})['value']
    eventvalidation = bs.find('input', {'id': '__EVENTVALIDATION'})['value']
    return viewstate, eventvalidation

def log_in():
    """提交用户名、密码和验证码，以及通过获取得到的表单其他项，登录教务系统"""
    login_url = 'jwc_glxt/Login.aspx'
    # 登陆按钮图片尺寸：69*43
    login_info = {'__VIEWSTATE': viewstate,
                  '__EVENTVALIDATION': eventvalidation,
                  'txtUserName': name,
                  'txtPassword': password,
                  'CheckCode': captcha,
                  'btnLogin.x': "57",
                  'btnLogin.y': "23"}
    r = s.post(host+login_url, data=login_info)
    # time.sleep(1)
    if r.status_code == 200:
        print('\t登录系统：成功')
    else:
        print('\t登录系统：失败')

def log_out():
    """登出教务系统"""
    logout_url = 'jwc_glxt/Login.aspx?xttc=1'
    xttc = s.get(host+logout_url)
    print(separating)
    # time.sleep(1)
    if xttc.status_code == 200:
        print('\t登出系统：成功')
    else:
        print('\t登出：失败')
    return xttc.status_code

