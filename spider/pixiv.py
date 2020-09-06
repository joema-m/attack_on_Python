import re
import threading
import selenium
from bs4 import BeautifulSoup as bs
import requests
import os
import json
from selenium import webdriver
import time
import pyautogui
from selenium.webdriver import ActionChains
from urllib.parse import quote, unquote

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/84.0.4147.105 Safari/537.36',
    'Connection': 'keep-alive',
    'referer': ""
}

rooturl = "https://www.pixiv.net/"
proxies = {'https': 'socks5://127.0.0.1:10808'}
# 保存路径
rootpath = './'
# web驱动路径
path = r'C:\Users\majun\Anaconda3\envs\spider\chromedriver.exe'
b = webdriver.Chrome(executable_path=path)
# artwork页面下第一张图片的xpath, 用于右键保存的，不过不靠谱
x_path = '#root > div:nth-child(2) > div.sc-1nr368f-2.gluvRx > div:nth-child(5) > div > section > ' \
         'div:nth-child(2) > div > ul > li:nth-child({}) > div > div.iasfms-1.BkIIg > div > a'

login_url = 'https://accounts.pixiv.net/login'
user_xpath = '//*[@id="LoginComponent"]/form/div[1]/div[1]/input'
passwd_xpath = '//*[@id="LoginComponent"]/form/div[1]/div[2]/input'
submit_xpath = '//*[@id="LoginComponent"]/form/button'
# 账号和密码
pixiv_user = '***'
pixiv_passwd = '***'


# 多线程下载，一个artworks页面就是一个线程
class MultiUrl(threading.Thread):
    def __init__(self, url, path):
        threading.Thread.__init__(self)
        self.url = url
        self.path = path

    def run(self):
        res_download(self.url, self.path)


# url是artworks，一次传递一个，外面可以实现多线程
def res_download(url, path):
    if not os.path.exists(path):
        os.mkdir(path)
    # 其实这里没必要修改referer，用root_url就行，刚开始不懂，以为要根据不同的artworks页面修改成相应的
    headers['referer'] = url
    # 这里获取这个页面的original 图片
    imgs = get_original(url)
    for img in imgs:
        res = requests.get(img, headers=headers, proxies=proxies)
        if res.status_code == 200:
            filename = img.split(r'/')[-1]
            with open(os.path.join(path, filename), 'wb') as f:
                print('downloading', filename)
                f.write(res.content)
        else:
            print(res.status_code)


# 这样只能获取第一张图片
# 要获取全部的， 还需要动态加载,  等等， 有一个 pageCount 参数
# 先试试获取一张
def get_original(url):
    """
    获取一个artworks页面下的所有图片
    :param url: 一条artworks的url
    :return: imgs列表
    """
    artworkid = url.split(r'/')[-1]
    res = requests.get(url, proxies=proxies)
    imgs = []
    if res.status_code == 200:
        soup = bs(res.content, 'html5lib')
        l = soup.find_all('meta')
        j = json.loads(l[-1]['content'])
        pageCount = j['illust'][artworkid]["userIllusts"][artworkid]["pageCount"]
        p0 = j['illust'][artworkid]['urls']['original']
        imgs.append(p0)
        for i in range(1, pageCount):
            imgs.append(p0.replace('p0', 'p' + str(i)))
    return imgs


def get_links_from(HTML):
    """
    由于pixiv是动态加载的，直接获取页面不可行，有两种方式
    1.保存页面，获取html文件
    2.selenium模拟登录
    这里采用第一种方式
    :param HTML: 下载的html文件
    :return: artworks的url列表
    """
    links = []
    with open(HTML, 'r', encoding='utf-8') as f:
        res = f.read()
    soup = bs(res, 'html5lib')
    objects = soup.find_all('a', href=re.compile(r'net/artworks/'))
    for i in objects:
        links.append(i['href'])
    sets = set(links)
    return sets


def get_links_from_url(url, login):
    """

    :param url: 搜索页面
    :param login: 是否登录
    :return: artworks的链接列表
    """
    url = url
    if login:
        login()
    links = []
    b.get(url)
    time.sleep(2)
    for i in range(1, 5):
        js = "var q=document.documentElement.scrollTop={}".format(i * 1000)
        b.execute_script(js)
        time.sleep(3)
    res = b.page_source
    soup = bs(res, 'html5lib')
    # objects = soup.find_all('a', href=re.compile('artworks/'))
    # 从用户页面获取
    objects = soup.find_all('a', href=re.compile(r'^/artworks/[0-9]'))
    for i in objects:
        links.append(rooturl + i['href'].strip(r'/'))
    sets = set(links)
    return sets


def login():
    """
    登录pixiv
    :return:
    """
    user = pixiv_user
    passwd = pixiv_passwd
    b.get(login_url)
    time.sleep(2)
    b.find_element_by_xpath(user_xpath).clear()
    b.find_element_by_xpath(user_xpath).send_keys(user)
    time.sleep(3)
    b.find_element_by_xpath(passwd_xpath).clear()
    b.find_element_by_xpath(passwd_xpath).send_keys(passwd)
    time.sleep(5)
    b.find_element_by_xpath(submit_xpath).click()
    time.sleep(10)


def down(url, path, login):
    if not os.path.exists:
        os.mkdir(path)
    links = get_links_from_url(url, login=login)
    print('links :', len(links))
    time.sleep(2)
    for link in links:
        MultiUrl(link, path).start()
        time.sleep(3)


if __name__ == "__main__":
    # 可以修改最后面的p来获取不同的页面,这里就偷下懒
    search_url = 'https://www.pixiv.net/tags/%E3%82%A8%E3%83%AC%E3%83%9F%E3%82%AB/illustrations?p=1'
    search_name = unquote(search_url.split(r'/')[-2])
    path = os.path.join(rootpath, search_name)
    if not os.path.exists(path):
        os.mkdir(path)
    # 如果是搜索页面的话，不用登录
    down(search_url, path, login=False)


