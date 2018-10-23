# -*- coding: utf-8 -*-
import scrapy


# 第一种方式：直接携带cookies登录
class Login1Spider(scrapy.Spider):
    name = 'login1'

    def start_requests(self):
        url = 'https://www.douban.com/'  # 豆瓣
        cookies_str = '获取到的Cookie'
        # 将Cookie转换为字典
        cookies = {i.split('=')[0]: i.split('=')[1] for i in cookies_str.split(';')}
        yield scrapy.Request(url=url, cookies=cookies, callback=self.parse)

    def parse(self, response):
        # 查看是否登录成功，去寻找登录后的元素
        result = response.css('div.text a::text').extract()
        for item in result:
            print(item)

# scrapy中cookie不能够放在headers中，在构造请求的时候有专门的cookies参数，能够接受字典形式的coookie
# 在setting中设置ROBOTS协议、USER_AGENT
