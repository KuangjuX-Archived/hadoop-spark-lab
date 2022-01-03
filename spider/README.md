# 爬虫程序

## 说明
爬虫采用的 `asyncio` 来做异步爬取，首先获取 `cookie` 来模拟登录，随后从搜索页获取到会员的元信息，然后对元信息进行爬取，从元信息中获取到 `realUid` 之后进入到会员的主页获取详细信息，由于连续访问 10 条会员信息以上会被识别为爬虫，需要进行滑块验证，我们从页面中获取到完整的图片和有缺失的图片并进行逐像素比对，随后获取到滑块到像素的距离并进行模拟滑动。

## 引用
- [极验滑动验证码的识别-崔庆才](https://github.com/Python3WebSpider/Python3WebSpider/blob/master/8.2-%E6%9E%81%E9%AA%8C%E6%BB%91%E5%8A%A8%E9%AA%8C%E8%AF%81%E7%A0%81%E8%AF%86%E5%88%AB.md)
- [Crack the slider verification code of station B with Python + selenium, the road of information security](https://pythonmana.com/2021/08/20210819125058115g.html)
- [极验滑块破解-掘金](https://juejin.cn/post/6844903953595891725)