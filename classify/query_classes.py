#! /usr/bin/env python
# -*- coding:utf-8 -*-
# Name:爬取教务系统学生课表
# Version:0.1
# Author:4thirteen2one

import requests

s = requests.session()

class QueryClasses(object):
    def __init__(self):
        self.cho_year = ""
        self.cho_term = ""
        self.viewstate = ""
        self.eventvalidation = ""

    def choose_term(self):
        """选择学年和学期"""
        status1 = False
        status2 = False
        counter = 0
        while not (status1 and status2):
            # time.sleep(1)
            self.cho_year = input('\t请输入需要查询的学年：')
            print('\n\t[1：春季学期]  [3：秋季学期]\n')
            self.cho_term = input('\t请输入需要查询的学期：')
            status1 = 1996 <= int(cho_year) <= 2023
            status2 = (int(cho_term)==1) or (int(cho_term)==3)
            if status1 and status2:
                break
            else:
                counter += 1
                if counter >= 3:
                    print("\n\t你4不4傻？")
                else:
                    print("\n\t输入非法！请重新输入！")

    def get_page(self):
        """打开课程查询页面，选择学期，返回所选学期课程页面"""
        schedule_url = 'jwc_glxt/Course_Choice/Stu_Course_Query.aspx'
        self.viewstate, self.eventvalidation = aspx_id(host+schedule_url)
        select = {'__EVENTTARGET': '',
                  '__EVENTARGUMENT': '',
                  '__VIEWSTATE': viewstate,
                  '__EVENTVALIDATION': eventvalidation,
                  'ctl00$MainContentPlaceHolder$School_Year': year,
                  'ctl00$MainContentPlaceHolder$School_Term': term,
                  'ctl00$MainContentPlaceHolder$BtnSearch.x': '18',
                  'ctl00$MainContentPlaceHolder$BtnSearch.y': '3'}
        r = s.post(host+schedule_url, data=select)
        # time.sleep(1)
        if r.status_code == 200:
            print('\t获取课表：成功')
        else:
            print('\t获取课表：失败')
        return r