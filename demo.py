import requests
from bs4 import BeautifulSoup
import re
import urllib.request
import time
import random

# 获取一页内所有话题
def gethtml(url):
    res = requests.get(url)
    res.encoding = 'utf-8'
    # print(res.text)
    soup = BeautifulSoup(res.text,'html.parser')
    header = soup.select('.title')
    # print(header)
    for head in header:
        atitle = head.select('a')[0].text.strip()#抓取话题标题
        alink = head.select('a')[0]['href']#抓取话题链接
        print(atitle,alink)
        # getimg(alink,atitle)

# 获取标题下的所有图片
def getimg(inhtml,atitle):
    res = requests.get(inhtml)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    header = soup.select('.topic-richtext')
    # print(header)
    # print('==================')
    if len(header) >0:
        for head in header:
            alinkk = head.select('.image-container')
            i = 0
            for link in alinkk:
                # src = alinkk.select[0]['src']
                src = link.select('img')[0]['src']
                print(src)
                # img_name = re.findall(r'p\d{9}',src)[0]
                # print(img_name)
                img_name = atitle + '_' + str(i)
                # print(img_name)
                download_img = urllib.request.urlretrieve(src,'F:\\豆瓣抓取\\%s.jpg'%img_name)
                print('下载成功')
                i +=1
                sleeptime=random.randint(0, 15)
                print('休息'+str(sleeptime)+'秒')
                time.sleep(sleeptime)


if __name__ == '__main__':
    url = 'https://www.douban.com/group/DQMQQ/discussion?start='
    # 开始页
    beginpage = 6
    # 终止页码
    endpage = 10
    #开始话题
    begintopic = (beginpage-1)*25
    # 终止话题
    endtopic = (endpage-1)*25

    while begintopic<= endtopic:
        gethtml(url+str(begintopic))
        sleeptime = random.randint(0, 100)
        print('第'+str(begintopic/25+1)+'页抓取完毕,'+'暂停'+str(sleeptime)+'秒继续下载')
        begintopic = begintopic + 25
        time.sleep(random.randint(0, 100))
