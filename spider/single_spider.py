import requests
import random
import sys
import json
import csv
import re
from bs4 import BeautifulSoup
from json.decoder import JSONDecodeError
from threading import Lock
from slider_crack import SliderCracker

# 单线程爬虫抽象类
class SingleSpider:
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()
        self.headers = self.__get_user_agent()

    # 获取随机 User-Agent 头，防止被识别为爬虫
    def __get_user_agent(self):
        user_agent_list = [
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6',
        'Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)',
        'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6',
        'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.3 Mobile/14E277 Safari/603.1.30',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    ]

    # 获取代理 ip 地址
    def __get_proxy(self):
        try:
            proxy = requests.get("http://127.0.0.1:5555/random").text.strip()
            return proxy
        except Exception:
            print("[Exception]")
            sys.exit(-1)

# 世纪佳缘爬虫的具体类
class JSpider(SingleSpider):
    def __init__(self, url):
        # 调用父类的初始化方法
        super(JSpider, self).__init__(url)


    def __deep_search(self, id):
        url = "https://www.jiayuan.com/{}?fxly=search_v2".format(id)
        names = ['education', 'height', 'car', 'income', 'house', 'weight', 'constellation', 'nationality', 'zodiac', 'blood']
        response = self.session.get(url)
        if response.status_code == 200:
            html = BeautifulSoup(response.text, 'html.parser')
            try:
                results = html.find("ul", class_ = "member_info_list fn-clear").find_all('em')
                pattern = r"<.*?>(.*?)<.*?>"
                details = {}
                for (index, item) in enumerate(results):
                    info = re.findall(pattern, str(item)).pop()
                    details[names[index]] = info
                print(details)
                return details
            except AttributeError:
                print("[Error] 被屏蔽了")
                slider_cracker = SliderCracker(url)
                slider_cracker.crack()     
                return self.__deep_search(id)     

    def req(self, page: int, payload):
        response = self.session.post(url = self.url, data=payload)
        if response.status_code == 200:
            print('成功获取数据')
            data = response.text[11:]
            data = data[:-13]
            try:
                data = json.loads(data)
                return data
            except JSONDecodeError:
                print('[Error] JsonDecodeError in page {}'.format(page))
            return None
        else:
            print('失败获取数据')
            sys.exit(-1)
    
    # 提取用户信息并从个人主页中拿到更加详细的个人信息
    def extarct(self, data):
        extract_data = []
        keys = ['uid', 'nickname', 'sex', 'marriage', 'height', 'education', 'income', 'work_location', 'image', "randListTag", "randTag", "shortnote"]
        user_info = data['userInfo']
        for item in user_info:
            extract_item = {}
            for k, v in item.items():
                if k == 'uid' and v == 253091710:
                    continue
                elif k == 'realUid':
                    # 爬取用户更详细的信息
                    details = self.__deep_search(v)
                    extract_item = dict(extract_item, **details)
                elif k in keys:
                    filter_value = re.compile(r'<[^>]+>', re.S)
                    filter_value = filter_value.sub(' ', str(v))
                    extract_item[k] = filter_value
            extract_data.append(extract_item)
        return extract_data

    
    def store_csv(self, filename, data):
        with open(filename, 'a+', encoding='utf-8') as f:
            csv_writer = csv.writer(f)
            for item in data:
                info = [str(v) for v in item.values()]
                csv_writer.writerow(info)

    def run(self, page: int):
        payload = [
            ('sex', 'f'),
            ('key', ''), 
            ('stc', '23:1'),
            ('sn', 'default'),
            ('sv', '1'),
            ('p', str(page)),
            ('f', ''), 
            ('listStyle', 'bigPhoto'),
            ('pri_uid', '254091710'),
            ('jsversion', 'v5')
        ]
        data = self.req(page, payload)
        if data == None:
            return 
        else:
            flush_data = self.extarct(data)
            print(flush_data)
            self.store_csv("new_data.csv", flush_data)