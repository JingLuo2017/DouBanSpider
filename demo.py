# coding = utf-8
import logging
import random
import time
import urllib.request

import requests
from selenium import webdriver

# 实例化driver
# option= webdriver.ChromeOptions()
# driver = webdriver.Chrome(chrome_options=option)
driver = webdriver.Chrome('F:\\迅雷下载\\chromedriver_win32\\chromedriver.exe') # chromedirver所在路径
# 登陆
driver.get('https://accounts.douban.com/passport/login')
driver.find_element_by_class_name('account-tab-account').click()  # 模拟点击
time.sleep(2)
driver.find_element_by_id('username').send_keys('username')  # 输入用户名
driver.find_element_by_id('password').send_keys('password')  # 输入密码
driver.find_element_by_css_selector("[class='btn btn-account btn-active']").click()  # 模拟点击
time.sleep(5)
'''
TODO:验证码
'''
# 获取cookie
session = requests.Session()
cookies = driver.get_cookies()
for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'])
# print(cookies)
time.sleep(3)

logging.FileHandler(filename='Selenium_img_douban.log', encoding='utf-8')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %A %H:%M:%S',
                    filename='F:\\豆瓣下载\\Selenium_img_douban.log', # 日志保存路径
                    filemode='w')


def get_headers():
    '''
    随机获取一个headers
    '''
    user_agents = ['Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
                   'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
                   'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11']
    headers = {'User-Agent': random.choice(user_agents)}
    return headers


def get(url, start_page, end_page, params=None):
    '''
    向一个url发送get请求，返回response对象
    :param url: 网页链接
    :param params: URL参数字典
    :return: 发送请求后获取的response对象
    '''
    # 等待一个随机的时间，防止被封IP，这里随机等待0~6秒，亲测可有效地避免触发豆瓣的反爬虫机制
    time.sleep(6 * random.random())
    resp = session.get(url, params=params, headers=get_headers())
    print(resp)
    logging.info(resp)
    if resp:
        logging.info(
            '[get] url = {0}, status_code = {1}'.format(url, resp.status_code))
        resp.encoding = 'utf-8'
        # 这里很重要，每次发送请求后，都更新session的cookie，防止cookie过期
        if resp.cookies.get_dict():
            session.cookies.update(resp.cookies)
            logging.info('[get] updated cookies, new cookies = {0}'.format(
                resp.cookies.get_dict()))
    else:
        logging.info('[get] url = {0}, response is None'.format(url))
    logging.info('[info] 寻找小组列表地址...')
    logging.info('[get] 已进入小组首页')
    while start_page <= end_page:
        driver.get('https://www.douban.com/group/DQMQQ/discussion?start=' + str((start_page - 1) * 25)) # 晒晒你最性感的照片小组
        logging.info('已进入第' + str(start_page) + '页')
        print('已进入第' + str(start_page) + '页')
        # 每一页讨论链接列表
        links = driver.find_elements_by_xpath(r"//tbody/tr/td[@class='title']/a")
        topic_links = {}
        for link in links:
            topic_link = link.get_attribute('href')
            title_name = link.get_attribute('title')
            # 获取的图片以小组话题名称命名
            img_name = title_name.replace('?', '？').replace('\\', '').replace('/', '').replace('"', '').replace(':','').replace('*','').replace('<', '').replace('>', '').replace('|', '').replace('\n', '')
            topic_links[topic_link] = img_name
            topic_num = 0
        for topic_link, img_name in topic_links.items():
            logging.info('进入第' + str(start_page) + '页，第' + str(topic_num + 1) + '话题。')
            topic_num += 1
            driver.get(topic_link)
            # 判断该话题下有无图片
            img_links = driver.find_elements_by_class_name('image-wrapper')
            if len(img_links) > 0:
                i = 0
                for img_link in img_links:
                    img_name = topic_links[topic_link] + '_' + str(i)
                    img_src = img_link.find_element_by_xpath('./img').get_attribute('src')
                    print('[get] 话题：' + img_name + ', 图片链接：' + img_src)
                    download_img = urllib.request.urlretrieve(img_src, 'F:\\豆瓣下载\\%s.jpg' % img_name)
                    time.sleep(3 * random.random())
                    i += 1
            else:
                print('1该标题下无图片')
            img_links2 = driver.find_elements_by_css_selector("[class='topic-figure cc']")
            # # 小组讨论167页以后使用网页格式改变，使用下面代码
            # if len(img_links2) > 0:
            #     i = 0
            #     for img_link in img_links2:
            #         img_name = topic_links[topic_link] + '_' + str(i)
            #         img_src = img_link.find_element_by_xpath('./img').get_attribute('src')
            #         print('[get] 话题：' + img_name + ', 图片链接：' + img_src)
            #         download_img = urllib.request.urlretrieve(img_src, 'F:\\豆瓣下载\\%s.jpg' % img_name)
            #         time.sleep(3 * random.random())
            #         i += 1
            # else:
            #     print('2该标题下无图片')
            time.sleep(3 * random.random())
        start_page += 1
        time.sleep(3 * random.random())
    time.sleep(5)
    driver.quit()


if __name__ == '__main__':
    group_url = 'https://www.douban.com/'
get(group_url, 0, 346)
