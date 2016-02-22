#coding=utf-8
import re
import requests
import math

#write your id and password here
data={
    'username':'',
    'password':''
}


def convertTime(time):

    time=time+20*60

    hour=math.floor(time/3600)
    hour=int(hour)
    minutes=math.ceil((time-3600*hour)/60)
    minutes=int(minutes)

    strshowtime='已用时间: '
    strshowtime+=str(hour)
    strshowtime+='小时 '
    strshowtime+=str(minutes)
    strshowtime+='分钟'
    print(strshowtime)

def convertMoney(money):
    strlen=len(money)
    i=0
    newmoney=''
    for i in range(strlen):
        if(i==strlen-2):
            newmoney+='.'
        newmoney+=money[i]
    return newmoney


if __name__=='__main__':
    requesturl='http://p.nju.edu.cn/portal_io/login'

# url='http://p.nju.edu.cn'
# content=requests.get(url).content
# html=content.decode("utf8", "ignore")
# postfix=re.findall('href="(.*?)";',html)
# strpostfix=postfix[0]
# realurl=url+strpostfix




    postcontent=requests.post(requesturl,data=data).content
    posthtml=postcontent.decode("utf8", "ignore")
    #get login info and balance and name
    logininfogroup=re.findall('"reply_msg":"(.*?)"',posthtml)
    logininfo=logininfogroup[0]
    fullname='GoodDay! '
    fngroup=re.findall('"fullname":"(.*?)"',posthtml)
    fullname+=fngroup[0]
    balance='余额: '
    bagroup=re.findall('"balance":(.*?),',posthtml)



    print(fullname)
    print(logininfo)
    balance+=convertMoney(str(bagroup[0]))
    balance+='元'
    print(balance)

# getTime
    a='http://p.nju.edu.cn/portal_io/selfservice/volume/getlist'
    b='http://p.nju.edu.cn/portal_io/proxy/notice'
    requests.post(b)
    realcontent=requests.post(a).content
    realhtml=realcontent.decode("utf-8","ignore")

    strtimegroup=re.findall('"total_time":(.*?),',realhtml,re.S)
    time=int(strtimegroup[0])
    convertTime(time)



