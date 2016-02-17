#coding=utf-8
import re
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf8')

global pagenum, url, html,allcontent,f,songtotal

pagenum = 0
totalNum = 0
allcontent = []
songtotal=0;

def saveTotxt():
    global pagenum,allcontent,f,songtotal
    realpage=(pagenum+20)/20
    print('正在处理第'+str(realpage)+'页')
    cutline='-----------------------第'
    cutline+=str(realpage)
    cutline+='页-----------------------\n'
    f.writelines(cutline)
    for each in allcontent:
        f.writelines('歌名: '+each['title']+'\n')
        f.writelines('歌手: '+each['singer']+'\n')
        f.writelines('详细描述: '+each['des']+'\n')
        f.writelines('\n')
        songtotal=songtotal+1







def outputRes():
    global allcontent
    for each in allcontent:
        print('title: '+each['title'])
        print('singer: '+each['singer'])
        print('des: '+each['des'])
        print('')



def changePage():
    global pagenum, url,html
    pagenum = pagenum + 20
    substr = 'start='
    substr += str(pagenum)
    substr += '&size'
    url = re.sub('start=(.*?)&size', substr, url)
    contents = requests.get(url).content
    html = contents.decode("utf8", "ignore")


def getTotalPageNum():
    global html
    totalNum = 0
    numstr = re.search('<div class="page-inner">(.*?)</div>', html, re.S).group(0)

    allnum = re.findall('">(.*?)</a>', numstr)

    print(allnum)

    len = allnum.__len__()

    if (len == 0):
        totalNum = 1
    else:
        totalNum = allnum[len - 2]

        # print(totalNum)
    return totalNum


def getContent():
    maincontent = re.search(
        '<li data-songitem =(.*?)<a   href="javascript:;"  class="btn btn-b btn-disabled play-selected-hook" >', html,
        re.S).group(0)
    titlelist = re.findall('data-info=\'\'>(.*?)</a>', maincontent, re.S)
    singerlist = re.findall('author_list" title="(.*?)">', maincontent, re.S)
    descriptionlist = re.findall('\'title="(.*?)" data-film=', maincontent, re.S)

    listlen = titlelist.__len__()
    slen=singerlist.__len__()
    dlen=descriptionlist.__len__()

    if(listlen!=slen):
        print('百度的html又鬼畜了,跳过这一页')
        return
    if(listlen!=dlen):
        print('百度的html又鬼畜了,跳过这一页')
        return
    if(slen!=dlen):
        print('百度的html又鬼畜了,跳过这一页')
        return

    for i in range(listlen):
        info = {}
        info['title'] = titlelist[i]
        info['singer'] = singerlist[i]
        info['des'] = descriptionlist[i]
        allcontent.append(info)






if __name__=='__main__':

    # Rendering URL......
    rawurl = 'http://music.baidu.com/search/song?s=1&key='
    rawurl2 = '&jump=0&start='
    rawurl3 = '&size=20&third_type=0'
    name = raw_input("输入搜索关键词: ")
    url = rawurl + name + rawurl2 + str(pagenum) + rawurl3
    filename=name
    filename+='的搜索结果.txt'
    f=open(filename,'a')

    # GetCODE....
    content = requests.get(url).content
    html = content.decode("utf8", "ignore")

    # GETNUMTOTAL
    totalNum=int(getTotalPageNum())
    f.writelines('正在从百度音乐搜索引擎搜索 '+name+'...'+'\n')
    print(totalNum)
    f.writelines('共搜到结果 '+str(totalNum)+'页\n')

    for i in range(totalNum):
        getContent()
        #outputRes() print to console
        saveTotxt()
        if i!=totalNum-1:
            changePage()
        allcontent=[]

print('Success!')
f.writelines('共搜到结果 '+str(songtotal)+' 条结果\n')

