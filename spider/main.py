from single_spider import JSpider

def jsingle_main():
    url = 'https://search.jiayuan.com/v2/search_v2.php'
    spider = JSpider(url)
    for page in range(1, 100):
        spider.run(page)

if __name__ == '__main__':
    jsingle_main()