import re
import requests
import time

url='http://cn.bing.com'

html=requests.get(url).text
src=re.search('g_img=\{url:\'(.*?).jpg', html).group(0)
#print(html)

realurl=src[12:]


date = time.ctime()
pic = requests.get(realurl)
fp = open('wallpaper' + date +'.jpg', 'wb')
fp.write(pic.content)
fp.close()
print('Success!')



