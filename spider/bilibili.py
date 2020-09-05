import threading
from bs4 import BeautifulSoup as bs
import requests
import re
import time
from selenium import webdriver
import json
import os
from selenium.webdriver import ActionChains

driver_path = r'C:\Users\majun\Anaconda3\envs\spider\chromedriver.exe'

next_selector = '#page-article > div > div.main-content > ul > li.be-pager-next > a'
jump_selector = '#page-article > div > div.main-content > ul > span.be-pager-options-elevator > input'
max_page_selector = '#page-article > div > div.main-content > ul > span.be-pager-total'

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 '
                         'Safari/537.36'}
proxies = {'https': 'socks5://127.0.0.1:10808'}


class MultiChapter(threading.Thread):
    """
    多线程下载，每一章（一个cv页面)就是一个线程
    """

    def __init__(self, url, path):
        threading.Thread.__init__(self)
        self.url = url
        self.path = path

    def run(self):
        chapter_download(self.url, self.path)


def chapter_download(chapter_url, path):
    """
    单线程下载实现，
    调用get_images_and_title()获取images列表以及title，并新建目录
    调用download()下载图片
    :param chapter_url: 一个cv页面url
    :param path: 存储目录
    :return:
    """
    print('downloading: ', chapter_url)
    if not os.path.exists(path):
        os.mkdir(path)
    title, imgs = get_images_and_title(chapter_url)
    folder = chapter_url.split(r'/')[-1] + title.replace(r'/', '-')
    abs = os.path.join(path, folder)
    if not os.path.exists(abs):
        os.mkdir(abs)
    download(imgs, path=abs)
    print(chapter_url, 'done\n')


def get_images_and_title(url):
    """
    :param url: 一个cv页面的url
    :return: 此页面下的title以及所有图片url的列表
    """
    imgs = []
    res = requests.get(url)
    soup = bs(res.text, 'html5lib')
    objects = soup.find_all('img')
    title = soup.find('h1', class_="title").text
    p = re.compile('article')
    for i in objects:
        if re.search(p, str(i)):
            imgs.append('https://' + i['data-src'].split(r'//')[-1])
    return title, imgs


def download(imgs, path):
    """
    :param imgs: list类型，images的url列表
    :param path: 存储目录
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)
    for i in range(0, len(imgs)):
        postfix = imgs[i].split(r'.')[-1]
        filename = '%03d' % (i + 1) + '.' + postfix
        abspath = os.path.join(path, filename)
        if os.path.exists(abspath):
            print(abspath, 'exists')
            continue
        time.sleep(0.5)
        try:
            res = requests.get(imgs[i], headers=headers)
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
            print('超时或错误')
            continue
        if res.status_code == 200:
            if len(res.content) > 100 * 1000:
                print("downloading: ", imgs[i])
                with open(abspath, 'wb') as f:
                    f.write(res.content)
        else:
            print('error: ',res.status_code)


# # 将滚动条移动到页面的顶部
# js = "var q=document.documentElement.scrollTop=0"
# b.execute_script(js)
# time.sleep(3)
# for i in range(1, 10):
#     js = "var q=document.documentElement.scrollTop={}".format(i * 4000)
#     b.execute_script(js)
#     time.sleep(0.5)


def get_chapters(url, driver, page):
    """
    获取一个up的专栏链接
    :param url: 一个up的专栏页面
    :param driver: web驱动
    :param page: 下载页面的数目，如果大于总页面，则按最大的来，即下载全部
    :return: url:title的dict，考虑到有的title会重名，所以就这样存储
    """
    dicts = {}
    driver.get(url)
    time.sleep(5)
    max_page = driver.find_element_by_css_selector(max_page_selector).text
    p = re.compile(r'[0-9]+')
    max_page_num = int(re.findall(p, max_page)[0])
    print('max page num : ', max_page_num)
    j = min(page, max_page_num)
    while j:
        res = driver.page_source
        soup = bs(res, 'html5lib')
        objects = soup.find_all('a', href=re.compile(r'read/cv'))
        for i in range(0, len(objects), 3):
            # 有同名的文件夹，则把键值对反过来
            dicts['https:' + objects[i]['href']] = objects[i]['title']
        # 跳到下一页
        if j == 1:
            break
        j = j - 1
        next = driver.find_element_by_css_selector(next_selector)
        time.sleep(1)
        next.click()
        time.sleep(5)
    return dicts


def save_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    urls = []
    for i in data:
        urls.append(i)
    return urls


def begin(url, page, first):
    """
    开始下载
    :param url: up主的专栏页面
    :param page: 下载页面的数目
    :param first: 是否是第一次下载
    :return:
    """
    userid = url.split(r'/')[-2]
    filename = userid + '.json'
    if first:
        driver = webdriver.Chrome(executable_path=driver_path)
        urls = get_chapters(url=url, driver=driver, page=page)
        save_json(urls, filename=filename)
        urls = load_json(filename)
    else:
        urls = load_json(filename)
    for url in urls:
        MultiChapter(url=url, path='./' + userid).start()
        time.sleep(0.5)


if __name__ == '__main__':
    # 输入url即可
    url = 'https://space.bilibili.com/505394292/article'
    begin(url=url, page=1, first=True)
    # 单个cv下载
    # url = 'https://www.bilibili.com/read/cv5711088'
    # userid = url.split(r'/')[-2]
    # MultiChapter(url=url, path='./' + userid, begin=0).start()
