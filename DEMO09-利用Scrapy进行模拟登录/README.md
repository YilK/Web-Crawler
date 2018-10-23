# 利用 Scrapy 框架进行模拟登录

这个项目中一共3个Spider

[login1](https://github.com/YilK/Web-Crawler/blob/master/DEMO09-%E5%88%A9%E7%94%A8Scrapy%E8%BF%9B%E8%A1%8C%E6%A8%A1%E6%8B%9F%E7%99%BB%E5%BD%95/logining/spiders/login1.py)：模拟登录豆瓣

[login2](https://github.com/YilK/Web-Crawler/blob/master/DEMO09-%E5%88%A9%E7%94%A8Scrapy%E8%BF%9B%E8%A1%8C%E6%A8%A1%E6%8B%9F%E7%99%BB%E5%BD%95/logining/spiders/login2.py)：模拟登入github

[login3](https://github.com/YilK/Web-Crawler/blob/master/DEMO09-%E5%88%A9%E7%94%A8Scrapy%E8%BF%9B%E8%A1%8C%E6%A8%A1%E6%8B%9F%E7%99%BB%E5%BD%95/logining/spiders/login3.py)：模拟登录51cto

利用 Scrapy 模拟登入的方式有：

## 1.直接携带 cookies 进行登录

## 2.使用FromRequest类，提交Form表单数据实现登录





### 1.直接携带 cookies 进行登录

​	例子：登录豆瓣  =====[py文件](https://github.com/YilK/Web-Crawler/blob/master/DEMO09-%E5%88%A9%E7%94%A8Scrapy%E8%BF%9B%E8%A1%8C%E6%A8%A1%E6%8B%9F%E7%99%BB%E5%BD%95/logining/spiders/login1.py)

​	首先，你需要在PC端登录豆瓣，然后获取 Cookie 	—（在登录前右键检查，打开Network选项卡，去众多链接中寻找）。然后将其改变为字典类型，再提交

​	在settings.py中设置

```
USER_AGENT='Mozilla/5.0'#设置user-agent
ROBOTSTXT_OBEY = False
```

```python
# 第一种方式：直接携带cookies登录
class Login1Spider(scrapy.Spider):
    name = 'login1'

    def start_requests(self):
        url = 'https://www.douban.com/'  # 豆瓣
        cookies_str = '获取到Cookie'
        # 将Cookie转换为字典
        cookies = {i.split('=')[0]: i.split('=')[1] for i in cookies_str.split(';')}
        yield scrapy.Request(url=url, cookies=cookies, callback=self.parse)

    def parse(self, response):
        # 查看是否登录成功，去寻找登录后的元素
        result = response.css('div.text a::text').extract()
        for item in result:
            print(item)
```

​	需要注意：

```
# scrapy中cookie不能够放在headers中，在构造请求的时候有专门的cookies参数，能够接受字典形式的coookie
# 在setting中设置ROBOTS协议、USER_AGENT
```

### 2.使用FromRequest类，提交Form表单数据实现登录

​	1.分析登录时需要提交的信息(github为例子)=====[py文件](https://github.com/YilK/Web-Crawler/blob/master/DEMO09-%E5%88%A9%E7%94%A8Scrapy%E8%BF%9B%E8%A1%8C%E6%A8%A1%E6%8B%9F%E7%99%BB%E5%BD%95/logining/spiders/login2.py)

​	打开登录界面-->打开Network选项卡，在 Preserve log上✔-->在登入界面输入账号密码登录--->查看选项卡下各	链接下的信息(找到Form Data所在的数据块)可看到需要提交的数据，然后在General中可以看到请求的URL

```python
'commit': 'Sign in',
'utf8': '✓',
'authenticity_token': 一大串,
'login': '账号',
'password': '密码'
```

​	authenticity_token 信息未知 去登录页面可以找到找 authenticity_token对应的字段

​	2.开始前准备

​		在settings.py中设置

```
USER_AGENT='Mozilla/5.0'#设置user-agent
ROBOTSTXT_OBEY = False
COOKIES_ENABLED = True
```

​	3.获取 authenticity_token

```python
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
                'login': 'YilK',
                'password': 'hjkkk123456'
            }, callback=self.after_login)
```

​		需要注意：

​		meta：字典格式的元数据，可以传递给下一个函数[meta官网解释](https://doc.scrapy.org/en/latest/topics/request-response.html?highlight=cookiejar#scrapy.http.Request.meta)；
​		cookiejar：是meta的一个特殊的key，通过cookiejar参数可以支持多个会话对某网站进行爬取，可以对cookie做标记，1,2,3,4......这样scrapy就维持了多个会话；	

​		Scrapy提供了FormRequest类，是Request类的扩展，专门用来进行Form表单提交。我们主要使用FormRequest.from_response()方法来模拟简单登陆，通过FormRequest.from_response提交后，交给回调函数处理。代码如下：

```python
def after_login(self, response):
    # print(response.text)
    print('1111')
    # 查看是否有标题信息，这个标题是在登录之后才有的,如果有说明登录成功
    list = response.css('div h2').extract()
    print(list)
```





最后还有一个模拟登录 51cto 的例子  ===[py文件](https://github.com/YilK/Web-Crawler/blob/master/DEMO09-%E5%88%A9%E7%94%A8Scrapy%E8%BF%9B%E8%A1%8C%E6%A8%A1%E6%8B%9F%E7%99%BB%E5%BD%95/logining/spiders/login3.py)

