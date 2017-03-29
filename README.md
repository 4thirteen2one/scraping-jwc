# soc2ics4CTGU
(Schedule of Courses to ics document for CTGU)
## ???
??Python?????????????????????????????????????`*.ics`?????????outlook?gmail???????????????????????????

## ???Python???
requests???????
BeautifulSoup4?????????
re??????????????
getpass????????????????
uuid???????????ics???????????????
datetime????????
os??windows????????startfile???????????

## ??
- ??????[http://jwc.ctgu.edu.cn/](http://jwc.ctgu.edu.cn/fwqxztt.asp)??aspx??????????session??Cookie????????????__VIEWSTATE?__EVENTVALIDATION??????????????
- ??????????????????????Tesseract????????????????????????????????????????????????
- ics???Microsoft Outlook 2002 ???????? iCalendar ???????????????

## ????
1. ???????????????
![screenshot1](https://github.com/4thirteen2one/scraping-jwc/blob/master/screenshots/screenshot1.PNG)
2. ???????????
![screenshot2](https://github.com/4thirteen2one/scraping-jwc/blob/master/screenshots/screenshot2.PNG)
3. ???????????__VIEWSTATE?__EVENTVALIDATION?
4. ???????????????
5. ?????????
6. ??__VIEWSTATE?__EVENTVALIDATION????????????
7. ????????
![screenshot3](https://github.com/4thirteen2one/scraping-jwc/blob/master/screenshots/screenshot3.PNG)
8. ????????????????????
9. ????????????????`*.ics`??


## ????????????
- __VIEWSTATE & __EVENTVALIDATION
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
????????60\*25?
```
<img id="ImageCheck" 
    title="??????!????,????!"
    src="ValidateCode.aspx" 
    style="border-width:0px;" />
```

- schedule table
????????
```
<table class="GridViewStyle" 
       rules="all" 
       id="ctl00_MainContentPlaceHolder_GridScore_Q" 
       style="border-collapse:collapse;" 
       cellspacing="0" border="1">
```

- query
[????????????](http://210.42.38.26:84/jwc_glxt/Course_Choice/Stu_Course_Query.aspx)
????id?'ctl00$MainContentPlaceHolder$School_Year'
????id?'ctl00$MainContentPlaceHolder$School_Term'
?????????????????42\*17??
    'ctl00$MainContentPlaceHolder$BtnSearch.x'
    'ctl00$MainContentPlaceHolder$BtnSearch.y'

- ics??

?????
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
????
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