import asyncio
from single_spider import JiaYuanSpider, ZhenAiSpider
import os
import sys
from threading import Lock

from async_spider import AsyncJiaYuanSpider

# 获取账户信息
def get_account():
    if not os.path.exists("account.txt"):
        username = input("请输入用户名: ")
        password = input("请输入密码: ")
        with open("account.txt", "w+") as account:
            account.write(username)
            account.write("\n")
            account.write(password)
    else:
        with open("account.txt", "r+") as account:
            username = account.readline()
            password = account.readline()
    print("您的用户名为: {}".format(username))
    print("您的密码为: {}".format(password))
    return (username, password)

def get_cookies():
    if not os.path.exists("cookie.txt"):
        cookie = input("请输入 Cookie: ")
        with open("cookie.txt", "w+") as cookie_txt:
            cookie_txt.write(cookie)
    else:
        cookie_txt = open('cookie.txt', 'r+')
        cookie = cookie_txt.readline()
        cookie_txt.close()
    print("Cookie 为 {}".format(cookie))
    return cookie

def single_jiayuan_main():
    cookie = get_cookies()
    url = 'https://search.jiayuan.com/v2/search_v2.php'
    spider = JiaYuanSpider(url, cookie, "data/世纪佳缘-测试.csv")
    for page in range(1, 2):
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
        spider.run(page, payload)

def single_zhenai_main():
    url = "http://www.zhenai.com/zhenghun"
    spider = ZhenAiSpider(url, "data/珍爱.csv")
    spider.run()

async def async_jiayuan_main():
    if(len(sys.argv) < 4):
        print("[Error] 至少需要四个参数")
        sys.exit(-1)
    start_page = sys.argv[1]
    end_page = sys.argv[2]
    filename = sys.argv[3]
    cookies = get_cookies()
    write_lock = Lock()
    url = "https://search.jiayuan.com/v2/search_v2.php"
    spider = AsyncJiaYuanSpider(url, cookies, filename, write_lock)
    for page in range(int(start_page), int(end_page)):
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
        run_task = asyncio.create_task(spider.run(page, payload))
        await run_task
    
        

if __name__ == '__main__':
    # asyncio.run(async_jiayuan_main())
    # single_jiayuan_main()
    asyncio.run(async_jiayuan_main())