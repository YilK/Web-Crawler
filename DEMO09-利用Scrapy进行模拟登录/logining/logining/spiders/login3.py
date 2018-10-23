# -*- coding: utf-8 -*-
import scrapy


class Login3Spider(scrapy.Spider):
    name = 'login3'

    def start_requests(self):
        login_url = 'http://home.51cto.com/index'  # 登录页面
        yield scrapy.Request(url=login_url, meta={'cookiejar': 1}, callback=self.cto_login)

    def cto_login(self, response):
        # 找出表单中需要的数据  _csrf
        csrf = response.css('meta[name=csrf-token]::attr(content)').extract_first()
        print(csrf)
        yield scrapy.FormRequest.from_response(response=response,
                                               meta={'cookiejar': response.meta['cookiejar']},
                                               formdata={
                                                   '_csrf': csrf,
                                                   'LoginForm[username]': '账号',
                                                   'LoginForm[password]': '密码',
                                                   'LoginForm[rememberMe]': '0',
                                               },
                                               callback=self.after_login)

    def after_login(self, response):
        # 找到一个存储有自己信息的页面
        test_url = 'http://home.51cto.com/home'
        yield scrapy.Request(url=test_url, meta={'cookiejar': response.meta['cookiejar']}, callback=self.parse)

    def parse(self, response):
        # 查找自己的名称，如果找到了说明已经完成登录
        name = response.css('div.name a::text').extract_first()
        print(name)
