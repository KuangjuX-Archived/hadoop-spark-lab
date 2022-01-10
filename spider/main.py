from single_spider import JSpider, ZSpider
import os

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

def get_cookie():
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

def jsingle_main():
    (username, password) = get_account()
    cookie = get_cookie()
    url = 'https://search.jiayuan.com/v2/search_v2.php'
    spider = JSpider(url, username, password, cookie)
    # spider.login()
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

def zsingle_main():
    url = "http://www.zhenai.com/zhenghun"
    spider = ZSpider(url)
    spider.run("data/珍爱网.csv")
        

if __name__ == '__main__':
    # zsingle_main()
    jsingle_main()