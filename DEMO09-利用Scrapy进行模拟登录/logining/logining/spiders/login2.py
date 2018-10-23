# -*- coding: utf-8 -*-
import scrapy


# 第二种方式：使用FromRequest类，提交Form表单数据实现登录
class Login2Spider(scrapy.Spider):
    name = 'login2'

    def start_requests(self):
        url = 'https://github.com/login'
        # cookiejar：是meta的一个特殊的key，通过cookiejar参数可以支持多个会话对某网站进行爬取，
        # 可以对cookie做标记，1,2,3,4......这样scrapy就维持了多个会话；
        yield scrapy.Request(url=url, meta={'cookiejar': 1}, callback=self.parse)

    def parse(self, response):
        # 获取 authenticity_token
        authenticity_token = response.css('div input[name="authenticity_token"]::attr(value)').extract_first()
        print(authenticity_token)
        yield scrapy.FormRequest.from_response(
            response=response,
            meta={'cookiejar': response.meta['cookiejar']},  # 同一个会话
            formdata={
                'commit': 'Sign in',
                'utf8': '✓',
                'authenticity_token': authenticity_token,
                'login': '账号',
                'password': '密码'
            }, callback=self.after_login)

    def after_login(self, response):
        # print(response.text)
        print('1111')
        # 查看是否有标题信息，这个标题是在登录之后才有的,如果有说明登录成功
        list = response.css('div h2').extract()
        print(list)
