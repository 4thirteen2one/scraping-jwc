# soc2ics4CTGU
(Schedule of Courses to ics document for CTGU)

## 功能
基于Python，模拟登录三峡大学教务管理系统，获取已选课程列表网页内容并解析，将解析所得课程事件信息逐条写入`*.ics`格式的日历文件中，以供通过outlook或gmail等打开导入邮箱账户进行云端同步至每个已登录邮箱账号的设备中

## 所用Python模块
`requests`：向服务器请求网页内容

`BeautifulSoup4`：通过标签树解析返回网页

`re`：匹配并获取符合特定要求的文本内容

`getpass`：隐藏输入密码，保障账号安全

`uuid`：基于时间戳生成唯一标识码提供给ics文件中课程事件

`datetime`：设定日期和时间

`os`：windows下使用os.startfile调用软件打开验证码图片

## 背景
- 教务管理系统 [http://jwc.ctgu.edu.cn/](http://jwc.ctgu.edu.cn/fwqxztt.asp) 使用的aspx架构，所以不但要通过requests.session保存Cookie会话，还要及时更新下次提交表单时所需的`__VIEWSTATE` 和 `__EVENTVALIDATION` 值

- 由于之前使用Tesseract自动识别验证码时的准确率不高（当然也可能是我提供的训练样本数量不够的原因），所以在这里我选择了最原始的方法——在系统中打开验证码图片，通过肉眼观察得到验证码再进行输入

- ics 文件是 Microsoft Outlook 2002 或更高版本创建的 iCalendar 格式文件，受到广泛支持，可导入日历后进行云同步

## 工作流程
1. 选择登录端口
![screenshot1](https://github.com/4thirteen2one/scraping-jwc/blob/master/screenshots/screenshot1.PNG)

2. 输入用户名及密码，获取并输入验证码
![screenshot2](https://github.com/4thirteen2one/scraping-jwc/blob/master/screenshots/screenshot2.PNG)

3. 获取所提交表单中必需的 `__VIEWSTATE`和 `__EVENTVALIDATION` 值

4. 提交表单数据，登录教务管理系统

5. 更新查询课表提交表单中所需的 `__VIEWSTATE`和 `__EVENTVALIDATION` 值

6. 选择学年和学期，查询已选课表

7. 退出教务系统，准备开始处理获取到的页面
![screenshot3](https://github.com/4thirteen2one/scraping-jwc/blob/master/screenshots/screenshot3.PNG)

8. 从页面中提取课程事件信息，备份至本地文本文件中

9. 设置学期开始时间，将课程信息逐一写入`*.ics`文件
![screenshot4](https://github.com/4thirteen2one/scraping-jwc/blob/master/screenshots/screenshot4.PNG)

10. 将所生成ics文件导入outlook日历
![screenshot5](https://github.com/4thirteen2one/scraping-jwc/blob/master/screenshots/screenshot5.PNG)

## 附：网页中的几个关键标签
- `__VIEWSTATE` & `__EVENTVALIDATION`
```
<input type="hidden" 
       name="__VIEWSTATE" 
       id="__VIEWSTATE" 
       value="/wEPDwUKMTQ4NjM5NDA3OWQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFCGJ0bkxvZ2luU077LK9itKNe3fhI7aoZZ+S5Ryo=" />
<input type="hidden" 
       name="__EVENTVALIDATION" 
       id="__EVENTVALIDATION" 
       value="/wEWBQKOmrqLAwKl1bKzCQKC3IeGDAK1qbSRCwLO44u1DVzfq830wXTY29pyqB1kTMdgWLfG" />
```

- chaptcha
(验证码图片尺寸: `60*25`)
```
<img id="ImageCheck" 
    title="不区分大小写!红色数字,黑色字母!"
    src="ValidateCode.aspx" 
    style="border-width:0px;" />
```

- schedule table
已选课表网页的表格标签
```
<table class="GridViewStyle" 
       rules="all" 
       id="ctl00_MainContentPlaceHolder_GridScore_Q" 
       style="border-collapse:collapse;" 
       cellspacing="0" border="1">
```

- query
查询已选课表的请求链接: `http://210.42.38.26:84/jwc_glxt/Course_Choice/Stu_Course_Query.aspx`

```
查询学年：id?'ctl00$MainContentPlaceHolder$School_Year'
查询学期：id?'ctl00$MainContentPlaceHolder$School_Term'
查询按钮(图标尺寸: 42\*17)
    'ctl00$MainContentPlaceHolder$BtnSearch.x'
    'ctl00$MainContentPlaceHolder$BtnSearch.y'
```

- ics文件
文件头内容
```
BEGIN:VCALENDAR
PRODID:-//CTGU//Schedule of Courses//CN
VERSION:2.0
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:Schedule of Courses
X-WR-TIMEZONE:Asia/Shanghai
...
END:VCALENDAR
```

事件内容
```
BEGIN:VEVENT
SUMMARY:????? ??(1?)
DTSTART;VALUE=DATE-TIME:20170317T080000
DTEND;VALUE=DATE-TIME:20170317T094000
DTSTAMP;VALUE=DATE-TIME:20170329T212937Z
UID:c11e96cc-1483-11e7-8749-1cb72c279624@CTGU
RRULE:FREQ=WEEKLY;COUNT=13;INTERVAL=1
DESCRIPTION:???
LOCATION:J-3216
END:VEVENT
```