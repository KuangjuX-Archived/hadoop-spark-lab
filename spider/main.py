from single_spider import JSpider, ZSpider
import time

def jsingle_main():
    url = 'https://search.jiayuan.com/v2/search_v2.php'
    spider = JSpider(url)
    for page in range(91, 200):
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