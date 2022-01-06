from single_spider import JSpider, ZSpider

def jsingle_main():
    url = 'https://search.jiayuan.com/v2/search_v2.php'
    spider = JSpider(url)
    for page in range(1, 100):
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
    url = "https://www.zhenai.com/api/search/getConditionData.do"
    spider = ZSpider(url)
    for page in range(1, 10):
        payload = {
            ('sex', '1'),
            ('workCity', '-1'),
            ('ageBegin', '-1'),
            ('ageEnd', '-1'),
            ('heightBegin', '-1'),
            ('heightEnd', '-1'),
            ('body', '-1'),
            ('multiEducation', '-1'),
            ('salaryBegin', '-1'),
            ('salaryEnd', '-1'),
            ('page', str(page)),
            ('pageSize', '20'),
            ('_', '1641479868103'),
            ('ua', 'h5/1.0.0/1/0/0/0/901045/0//0/0/97b254c7-1906-4f00-82f0-53adb10d15ba/0/0/83518767')
        }
        spider.run(page, payload)

if __name__ == '__main__':
    zsingle_main()