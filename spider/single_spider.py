import requests
from requests.cookies import RequestsCookieJar
import random
import sys
import json
import csv
import re
from bs4 import BeautifulSoup
from json.decoder import JSONDecodeError
from requests.models import ChunkedEncodingError
from slider_crack import SliderCracker

# 单线程爬虫抽象类
class SingleSpider:
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()
        self.headers = self.__get_user_agent()

    def __del__(self):
        print('[Debug] Spider finish and destory')

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

        headers = {
            "User-Agent" : random.choice(user_agent_list),\
        }
        return headers

    # 获取代理 ip 地址
    def __get_proxy(self):
        try:
            proxy = requests.get("http://127.0.0.1:5555/random").text.strip()
            return proxy
        except Exception:
            print("[Exception]")
            sys.exit(-1)

    def req(self, payload):
        response = self.session.post(url = self.url, data=payload, headers = self.headers)
        if response.status_code == 200:
            return response.text
        else:
            print('[Error] Fail to request url')
            return None

    # 持久化，写入到 csv 文件中
    def persist(self, filename, data):
        with open(filename, 'a+', encoding='utf-8') as f:
            csv_writer = csv.writer(f)
            if data == None:
                return 
            else:
                for item in data:
                    info = [str(v) for v in item.values()]
                    csv_writer.writerow(info)

    def run(self):
        pass

# 世纪佳缘爬虫的具体类
class JiaYuanSpider(SingleSpider):
    # 重载的构造函数，除了调用父类的构造函数外，还需要用户名和密码
    def __init__(self, url, cookies):
        super(JiaYuanSpider, self).__init__(url)
        self.login_url = 'https://passport.jiayuan.com/dologin.php?pre_url=http://www.jiayuan.com/usercp'
        jar = RequestsCookieJar()
        for cookie in cookies.split(';'):
            key, value = cookie.split('=', 1)
            jar.set(key, value)
        self.cookies = jar

    # 对个人信息进行更深的提取
    def __deep_search(self, id):
        url = "https://www.jiayuan.com/{}?fxly=search_v2".format(id)
        names = ['education', 'height', 'car', 'income', 'house', 'weight', 'constellation', 'nationality', 'zodiac', 'blood']
        try:
            response = self.session.get(url, headers = self.headers, cookies = self.cookies)
            if response.status_code == 200:
                html = BeautifulSoup(response.text, 'html.parser')
                try:
                    # 获取择偶标准
                    criteria_results = html.find("ul", class_ = "js_list fn-clear").find_all('li')
                    criterias = {}
                    # print(criteria_results)
                    age_pattern = '.*?龄：</span><div class="ifno_r_con">(.*?)<font.*?>'
                    height_pattern = '.*?高：</span><div class="ifno_r_con">(.*?)<font.*?>'
                    education_pattern = '.*?历：</span><div class="ifno_r_con">(.*?)<font.*?>'
                    nationality_pattern = '.*?族：</span><div class="ifno_r_con">(.*?)</div></li>'
                    marriage_pattern = '婚姻状况：</span><div class="ifno_r_con">(.*?)<font.*?>'
                    location_pattern = '.*?地：</span> \
<div class="ifno_r_con_1">(.*?)<font.*?>'
                    for(index, item) in enumerate(criteria_results):
                        age = re.findall(age_pattern, str(item))
                        height = re.findall(height_pattern, str(item))
                        education = re.findall(education_pattern, str(item))
                        nationality = re.findall(nationality_pattern, str(item))
                        marriage = re.findall(marriage_pattern, str(item))
                        location = re.findall(location_pattern, str(item))
                        criterias['age'] = None if len(age) == 0 else age[0]
                        criterias['height'] = None if len(height) == 0 else height[0]
                        criterias['education'] = None if len(education) == 0 else education[0]
                        criterias['nationality'] = None if len(nationality) == 0 else nationality[0]
                        criterias['marriage'] = None if len(marriage) == 0 else marriage[0]
                        criterias['location'] = None if len(location) == 0 else location[0]
                    print("[Debug] 择偶标准: {}".format(criterias))

                    # 获取用户的详细信息
                    user_results = html.find("ul", class_ = "member_info_list fn-clear").find_all('em')
                    pattern = r"<.*?>(.*?)<.*?>"
                    details = {}
                    for (index, item) in enumerate(user_results):
                        info = re.findall(pattern, str(item)).pop()
                        details[names[index]] = info
                    print("[Debug] 用户详细个人信息: {}".format(details))
                    return details
                except AttributeError:
                    print("[Error] 被屏蔽了")
                    slider_cracker = SliderCracker(url)
                    slider_cracker.crack()     
                    return self.__deep_search(id)   
        except ChunkedEncodingError as error:
            print("[Error] {}".format(error))
            return self.__deep_search(id)
        except requests.exceptions.SSLError as ssl_error:
            print("[Error] {}".format(ssl_error))
            return self.__deep_search(id)
        except Exception as err:
            print("[Error] {}".format(err))
            return self.__deep_search(id)

    def req(self, page: int, payload):
        data = super(JiaYuanSpider, self).req(payload)
        if data == None:
            return None 
        else:
            data = data[11:]
            data = data[:-13]
            try:
                data = json.loads(data)
                return data 
            except JSONDecodeError:
                print('[Error] json decode error in page {}'.format(page))
                return None
    
    # 提取用户信息并从个人主页中拿到更加详细的个人信息
    def extarct(self, data):
        if data == None:
            return None
        extract_data = []
        keys = ['uid', 'nickname', 'sex', 'marriage', 'height', 'education', 'income', 'work_location', 'image', "randListTag", "randTag", "shortnote"]
        user_info = data['userInfo']
        for item in user_info:
            extract_item = {}
            for k, v in item.items():
                if k == 'uid' and v == 253091710:
                    # 这是自己的 UID, 直接跳过
                    break
                elif k == 'realUid':
                    # 爬取用户更详细的信息
                    details = self.__deep_search(v)
                    # 对信息进行合并
                    extract_item = dict(extract_item, **details)
                    print("[Debug] 用户个人信息: {}".format(extract_item))
                elif k in keys:
                    filter_value = re.compile(r'<[^>]+>', re.S)
                    filter_value = filter_value.sub(' ', str(v))
                    extract_item[k] = filter_value
            extract_data.append(extract_item)
        return extract_data
    
    # 模拟登陆并获取对应的 cookie 以拿到更详细的信息
    def login(self, username, password):
        try:
            # 首先访问登录页，拿到所有有关登陆的信息
            response = self.session.get('http://login.jiayuan.com', headers = self.headers)
            if response.status_code == 200:
                html = BeautifulSoup(response.text, 'html.parser')
                # 获取所有 input 信息
                payload = {}
                for item in html.find_all('input'):
                    if item.get('name') != None:
                        payload[item.get('name')] = item.get('value')
                # 构造登录需要的 payload
                payload['name'] = username
                payload['password'] = password
                # print("[Debug] payload: {}".format(payload))
                try:
                    # 向登录 URL 发送请求
                    response = self.session.post(self.login_url, data = payload, headers = self.headers)
                    if response.status_code == 200:
                        print('[Debug] {}'.format(response.text))
                        if response.text.count(u'jump'):
                            print('[Debug] Success to login')
                        else:
                            print('[Debug] Fail to login')
                            sys.exit(-1)
                    else:
                        print("[Error] Fail to login, status code is {}".format(response.status_code))
                        self.login()
                except Exception as error:
                    print("[Error] Fali to login, error is {}".format(error))
                    # self.login()
                    sys.exit(-1)
            else:
                print("[Error] Fail to visit login page, status code is {}".format(response.status_code))
        except Exception as error:
            print("[Error] Fail to visit login page, error is {}".format(error))
            # self.login()
            sys.exit(-1)

        


    def run(self, page: int, payload: dict):
        print("[Debug] Spider is running in page {}".format(page))
        data = self.req(page, payload)
        flush_data = self.extarct(data)
        # self.persist("data/世纪佳缘.csv", flush_data)
            


class ZhenAiSpider(SingleSpider):
    def req(self, url, page):
        url += "/"
        url += str(page)
        print("[Debug] Request URL: {}".format(url))
        response = requests.get(url = url, headers = self.headers)
        if response.status_code == 200:
            return response.text
        else:
            print("[Error] Fail to request url: {}".format(url))


    # 解析页面
    def parse(self, data):
        if data != None:
            html = BeautifulSoup(data, 'html.parser')
            try:
                results = html.find("div", class_ = "g-list").find_all("div", class_ = "list-item")
                album_pattern = r'<a href="(.*?)" target=.*?">'
                img_pattern = r'<img.*?src="(.*?)"/>'
                location_pattern = r'居住地：</span>(.*?)</td>'
                sex_pattern = r'性别：</span>(.*?)</td>'
                marriage_pattern = r'婚况：</span>(.*?)</td>'
                height_pattern = r'<span class="grayL">.*?高：</span>(.*?)</td>'
                education_pattern = r'.*?历：</span>(.*?)</td>'
                introduction_pattern = r'<div class="introduce">(.*?)</div>'
                details = []
                for item in results:
                    # print(item)
                    detail = {}
                    # 获取所有个人信息
                    album = re.findall(album_pattern, str(item))
                    img = re.findall(img_pattern, str(item))
                    location = re.findall(location_pattern, str(item))
                    sex = re.findall(sex_pattern, str(item))
                    marriage = re.findall(marriage_pattern, str(item))
                    height = re.findall(height_pattern, str(item))
                    eduction = re.findall(education_pattern, str(item))
                    introduction = re.findall(introduction_pattern, str(item))
                    # 将个人信息加入到字典中
                    detail['album'] = None if len(album) == 0 else img[0]
                    detail['img'] = None if len(img) == 0 else img[0]
                    detail['location'] = None if len(location) == 0 else location[0]
                    detail['sex'] = None if len(sex) == 0 else sex[0]
                    detail['marriage'] = None if len(marriage) == 0 else marriage[0]
                    detail['height'] = None if len(height) == 0 else height[0]
                    detail['education'] = None if len(eduction) == 0 else eduction[0]
                    detail['introduction'] = None if len(introduction) == 0 else introduction[0]
                    details.append(detail)
                return details
            except AttributeError:
                print("[Error] Fail to parse data.")
                return None
        else:
            print("[Error] Data is None")
            return None

    def get_all_url(self):
        base_url = "https://www.zhenai.com/zhenghun"
        response = requests.get(base_url, headers = self.headers)
        if response.status_code == 200:
            data = response.text
            pattern = '<a data-v-1573aa7c="" href="(.*?)">.*?</a>'
            html = BeautifulSoup(data, "html.parser")
            table = html.find("dl", class_ = "city-list clearfix")
            all_city_url = re.findall(pattern, str(table))
            self.url_list = all_city_url
        else:
            print('[Error] Fail to visit {}'.format(base_url))
            sys.exit(-1)

    def run(self, filename):
        super(ZhenAiSpider, self).run()
        self.get_all_url()
        for url in self.url_list:
            for page in range(1, 7):
                data = self.req(url, page)
                details = self.parse(data)
                self.persist(filename, details)




    