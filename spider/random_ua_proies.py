import random
import re
import requests
from lxml import etree
import subprocess as sp
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/84.0.4147.105 Safari/537.36',
    'Connection': 'keep-alive',
}

user_agent = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 "
    "Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 "
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]


# 下面来获取代理ip
# 首先要找一个靠谱的免费代理网站
# 例如：https://www.kuaidaili.com/free/intr/
# 测试过后才知道这里的代理连不上，虽然能ping通，port也没问题
# 下面来自动获取ip以及端口号
def get_proxies(pages=2):
    """
    :param pages: 爬取页面的数量，默认为1
    :return: proxies列表
    """
    proxies = []
    root_url = 'https://www.kuaidaili.com/free/intr/'

    for page in range(1, pages + 1):
        url = root_url + str(page)
        res = requests.get(url, headers=headers)
        selector = etree.HTML(res.text)
        ips = selector.xpath("//tbody/tr/td[@data-title='IP']")
        ports = selector.xpath("//tbody/tr/td[@data-title='PORT']")
        for i in range(0, len(ips)):
            print(ips[i].text + ':' + ports[i].text)
            # 测试是否能ping通
            cmd = "ping -n 2 " + ips[i].text
            p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
            # 获得返回结果并解码
            out = p.stdout.read().decode("gbk")
            p = re.compile('丢失 = [0-9]')
            lost = int(re.findall(p, out)[0].split('=')[-1])
            if lost < 1:
                proxies.append({"http": "http://" + ips[i].text + ":" + ports[i].text})
    return proxies


# 随机选取代理，如果在使用过程中连接超时，则删除
url = 'https://www.baidu.com'
# 随机选择UA构成头部信息
ua = random.choice(user_agent)
headers['User-Agent'] = ua

proxies = get_proxies()
proxy = random.choice(proxies)
try:
    # 如果响应超过三秒，或连接失败，则删除此代理
    res = requests.get(url, headers=headers, proxies=proxy, timeout=3)
except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
    proxies.remove(proxy)

