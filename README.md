# scraping-jwc

## get_schedule
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
```
<img title="??????!????,????!" 
     id="ImageCheck" 
     style="border-width:0px;" 
     src="ValidateCode.aspx">
```

- schedule table
```
<table class="GridViewStyle" 
       rules="all" 
       id="ctl00_MainContentPlaceHolder_GridScore" 
       style="border-collapse:collapse;" 
       cellspacing="0" border="1">
```

- query
```
?????http://jwc.ctgu.edu.cn:81/jwc_glxt/Course_Choice/Course_Schedule.aspx
id="ct100_Menu1n9"
????id="ctl00_MainContentPlaceHolder_GridScore"
?????id="ctl00_MainContentPlaceHolder_Label1"
?????id="ctl00_MainContentPlaceHolder_School_Year"
?????id="ctl00_MainContentPlaceHolder_School_Term"
???id="ctl00_MainContentPlaceHolder_BtnSearch"
```
