# 向登录接口POST表单数据
import requests
from scrapy import Selector
import re
from PIL import Image


class Login(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
        }
        self.login_url = 'https://accounts.douban.com/login'  # 登录界面的url
        self.session = requests.Session()  # 会话维持

    # 找到提交表单所需要的验证码图片与captcha_id
    def images(self):
        response = self.session.get(self.login_url, headers=self.headers)
        print(response)
        # 使用了Scraoy中的Selector，建立一个选择器对象，然后调用css()来提取信息
        selector = Selector(text=response.text)
        # 找到验证码图片的url
        images_url = selector.css('div img.captcha_image::attr(src)').extract_first()
        if images_url:  # 如果登录时需要验证码
            match = re.search(r'id=(\w+:en)', images_url)  # 使用正则表达式匹配出captcha-id
            if match:
                captcha_id = match.group(1)
                # print(captcha_id)
            # 将验证码图片存储起来，以便后续使用
            path = 'D://IDE//Pycharm//《网络爬虫实战开发》//模拟登录//' + captcha_id[:4] + '.jpg'
            r = requests.get(images_url)
            with open(path, 'wb') as f:
                f.write(r.content)
            # print(images_url)
        else:  # 没有找到验证码，就是登录时不需要验证码
            captcha_id = None
        return captcha_id

    def login(self):
        captcha_id = self.images()  # captcha—id
        # print(captcha_id)
        if captcha_id:  # 存在验证码
            image = Image.open('D://IDE//Pycharm//《网络爬虫实战开发》//模拟登录//' + captcha_id[:4] + '.jpg')
            image.show()  # 显示图片
            captcha_solution = input('请输入验证码:')
            FormData = {  # 表单数据
                'source': 'index_nav',
                'redir': 'https://www.douban.com/',
                'form_email': '账号',
                'form_password': '密码',
                'captcha-solution': captcha_solution,
                'captcha-id': captcha_id
            }
        else:  # 不存在验证码时提交的表单数据
            FormData = {
                'source': 'index_nav',
                'redir': 'https://www.douban.com/',
                'form_email': '账号',
                'form_password': '密码'
            }
        response = self.session.post(self.login_url, data=FormData, headers=self.headers)
        if response.status_code == 200:
            print('success')
        response = self.session.get('https://www.douban.com/explore/', headers=self.headers)  # 查看豆瓣页面下的其他信息
        if response.status_code == 200:
            print(response.text)


if __name__ == '__main__':
    login = Login()
    login.login()
