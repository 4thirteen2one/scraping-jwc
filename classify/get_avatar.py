#! /usr/bin/env python
# -*- coding:utf-8 -*-
import os,requests

def get_avatar(years,classes,numbers):
    stu_num = years+classes+numbers
    avatar_url = 'http://jwc.ctgu.edu.cn:84/jwc_glxt/Stu_Info/StuImageHandler.ashx?PhotoId={}'.format(stu_num)
    s = requests.session()
    r = s.get(avatar_url,stream=True)
    avatar = r.content
    with open('{}.jpg'.format(stu_num),'wb') as jpg:
        jpg.write(avatar)
    os.startfile('{}.jpg'.format(stu_num))

if __name__ == '__main__':
    years = input('请输入学年：')
    classes = input('请输入班级：')
    numbers = input('请输入学号：')
    get_avatar(years,classes,numbers)
