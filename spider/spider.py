from json.decoder import JSONDecodeError
from math import sin
import time
import requests
import random
import sys
import json
import csv
import re
from bs4 import BeautifulSoup
import asyncio
from threading import Lock
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class SliderCrack:
    def __init__(self, url, cookie):
        option = webdriver.ChromeOptions()
        option.add_argument("user-data-dir=D:\python-3.7.8\profile")
        self.url = url 
        self.browser = webdriver.Chrome(chrome_options=option)
        self.cookie = cookie
        # 为打开的网页添加cookie
        # self.browser.add_cookie(cookie)
        self.wait = WebDriverWait(self.browser, 20)

    def open_page(self):
        self.browser.get(self.url) 
        button = self.get_geetest_button()
        button.click()
        # self.browser.close()

    # 模拟点击
    def get_geetest_button(self):
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "geetest_slider_button")))
        return button

    def get_slider(self):
        """
        获取滑块
        返回：滑块对象
        """
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        return slider

    # 识别缺口
    def get_position(self):
        """
        获取验证码位置
        返回：验证码位置元组
        """
        img = self.wait.until(EC.presence_of_element_located(By.CLASS_NAME, 'geetest_canvas_bg geetest_absolute'))
        time.sleep(2)
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
        return (top, bottom, left, right)

    def get_geetest_image(self, name = 'captcha.png'):
        """
        获取验证码图片
        返回：图片对象
        """
        top, bottom, left, right = self.get_position()
        print('验证码位置: ', top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        return captcha

    def get_image_info(self):
        pass

class Spider:
    def __init__(self, url, cookie, mutex, viste_lock):
        self.url = url
        self.cookie = cookie.encode('utf-8').decode('latin1')
        self.mutex = mutex
        self.viste_lock = viste_lock
        self.ok_visit = True
    
    def GetUserAgent(self):
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

    async def _Deep_Search(self, id):
        url = "https://www.jiayuan.com/{}?fxly=search_v2".format(id)
        headers = self.GetUserAgent()
        headers['cookie'] = self.cookie
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            html = BeautifulSoup(response.text, 'html.parser')
            names = ['education', 'height', 'car', 'income', 'house', 'weight', 'constellation', 'nationality', 'zodiac', 'blood']
            try:
                results = html.find("ul", class_ = "member_info_list fn-clear").find_all('em')
                pattern = r"<.*?>(.*?)<.*?>"
                details = {}
                for (index, item) in enumerate(results):
                    info = re.findall(pattern, str(item)).pop()
                    details[names[index]] = info
                return details
            except AttributeError:
                print('[Error] AttributeError')
                self.viste_lock.acquire()
                self.ok_visit = False
                slide_crack = SliderCrack(url, self.cookie)
                slide_crack.open_page()
                self.ok_visit = True
                self.viste_lock.release()
                return {k: '--' for k in names}
        else:
            sys.exit(-1)

    async def Req(self, page: int):
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
        headers = self.GetUserAgent()
        headers['cookie'] = self.cookie
        response = requests.post(url = self.url, headers=headers, data=payload)
        if response.status_code == 200:
            print('成功获取数据')
            data = response.text[11:]
            data = data[:-13]
            try:
                data = json.loads(data)
            except JSONDecodeError:
                print('[Error] JsonDecodeError in page {}'.format(page))
                data = []
            return data
        else:
            print('失败获取数据')
            sys.exit(-1)
    
    async def Extarct(self, data):
        extract_data = []
        keys = ['uid', 'nickname', 'sex', 'marriage', 'height', 'education', 'income', 'work_location', 'image']
        user_info = data['userInfo']
        for item in user_info:
            extract_item = {}
            for k, v in item.items():
                if k == 'uid' and v == 253091710:
                    continue
                elif k == 'realUid':
                    while self.ok_visit == False:
                        time.sleep(1)
                    if self.ok_visit == True:
                        # task = asyncio.create_task(self._Deep_Search(v))
                        # details = await task
                        details = await self._Deep_Search(v)
                        extract_item = dict(extract_item, **details)
                elif k in keys:
                    extract_item[k] = v
            print(extract_item)
            extract_data.append(extract_item)
        return extract_data

    
    async def StoreCsv(self, filename, data):
        with open(filename, 'a+', encoding='utf-8') as f:
            csv_writer = csv.writer(f)
            for item in data:
                info = [str(v) for v in item.values()]
                self.mutex.acquire()
                csv_writer.writerow(info)
                self.mutex.release()

    async def Run(self, page: int, filename: str):
        # req_task = asyncio.create_task(self.Req(page))
        # data = await req_task
        data = await self.Req(page)
        if len(data) == 0:
            return
        # extract_task = asyncio.create_task(self.Extarct(data))
        # info = await extract_task
        info = await self.Extarct(data)
        # store_task = asyncio.create_task(self.StoreCsv(filename, info))
        # await store_task
        await self.StoreCsv(filename, info)


async def main():
    url = 'https://search.jiayuan.com/v2/search_v2.php'
    # cookie = 'guider_quick_search=on; accessID=20211202135956108286; save_jy_login_name=18630816527; stadate1=253091710; myloc=12%7C1207; myage=22; mysex=m; myuid=253091710; myincome=50; user_attr=000000; upt=8xrV2-DiJgNLaxEfnyzXCvYggkay2cZVhQleCdF3LRjMbBM6tbiuZ5iU1V093PEYrMmPrxDjsxV5o0bxv84np7sqEc8.; is_searchv2=1; skhistory_f=a%3A1%3A%7Bi%3A1640666916%3Bs%3A9%3A%22%E6%9C%89%E6%B0%94%E8%B4%A8%22%3B%7D; SESSION_HASH=8df3ef53fef81783d458aa67dee5f25d99c68d46; user_access=1; COMMON_HASH=b3537fe54438b10e458622110147b7e0; sl_jumper=%26cou%3D17%26omsg%3D0%26dia%3D0%26lst%3D2021-12-30; last_login_time=1640869075; PROFILE=254091710%3A%25E7%258B%2582%25E4%25B8%2594%3Am%3Aimages1.jyimg.com%2Fw4%2Fglobal%2Fi%3A0%3A%3A1%3Azwzp_m.jpg%3A1%3A1%3A50%3A10%3A3.0; PHPSESSID=8dd33c023609d323cc0cbc48b8865a88; pop_avatar=1; main_search:254091710=%7C%7C%7C00; RAW_HASH=MKP9%2Ahj-u3hydHEGb3RUB5jUlXOH9vtjjSdxRNPdWTANCeKcth3RIruSw4Ly0-ylwYG6z6QrhQ9%2Aex2PzY2HUyPkDdl9c3FeULCAWPKRpfOWQek.; pop_time=1640869108748'
    cookie_txt = open('cookie.txt', mode='r')
    cookie = cookie_txt.read()
    cookie_txt.close()
    tasks = []
    mutex = Lock()
    viste_lock = Lock()
    for page in range(1, 2):
        spider = Spider(url, cookie, mutex, viste_lock)
        task = asyncio.create_task(spider.Run(page, 'data.csv'))
        tasks.append(task)

    for task in tasks:
        await task

if __name__ == '__main__':
    asyncio.run(main())
    # driver = webdriver.Chrome()