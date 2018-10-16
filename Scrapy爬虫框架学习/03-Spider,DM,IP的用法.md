# Spider 的用法

# Downloader Middleware 的用法

# Item Pipeline 的用法





### 1. Spider的用法

1. **Spider运行流程**

   定义爬取网页的动作

   分析爬取下来的网页



   过程：

   以初始的URL初始化Request，并设置回调函数，当该Request成功请求并返回的时候，Response生成并作为参数传给该回调函数

   在回调函数分析返回的页面内容。返回的结果由两种形式。1、解析到有效字典或Item对象，通过处理后保存。2、解析到下一个连接，构造新的Request，返回Request等待后续调度

2. **基础属性**（部分）

   name：爬虫名称，是唯一的

   allowed_domains：运行爬取的域名，是可选的配置，不在此范围内的链接不会被爬取

   start_urls：它是起始的URL列表，当我们没有实现start_requests()方法时，默认这个列表开始抓取

   start_requests()：此方法用于生成初始请求，它必须返回一个可迭代对象。

   parse()：当Response没有指定回调函数时，该方法会被默认调用。它负责处理Response，处理返回的结果，并从中提取想要的数据和下一步请求

### 

### 2. Downloader Middleware 的用法

1. **作用位置**

   1.在Scheduler调度出队列的Request发送给Downloader之前，对Request进行修改

   2.在下载后生成的Response发送给Spider之前，对Response进行修改

2. **功能**

   修改User-Agent，处理重定向，设置代理，失败调试，设置Cookies

3. **核心方法**

   process_request(request, spider)

   process_response(request, response, spider)

   process_exception(request, exception, spider)

   至少实现一个方法，就可以定义一个 Downloader Middleware

   详细用法：https://scrapy-chs.readthedocs.io/zh_CN/latest/topics/downloader-middleware.html

4. **举例** （修改User-Agent）

   在middlewares.py 中添加一个RandomUserAgentMiddleware类

   ```python
   class RandomUserAgentMiddleware():
       def __init__(self):
           self.user_agent = [
               'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'
               'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'
               'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50'
               'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20'
           ]
       def process_request(self,request,spider):
           request.headers['User-Agent']=random.choice(self.user_agent)
   
   ```

   首先先定义了几个不同的User-Agent,然后实现 process_request(request, spider) 方法，修改request的headers属性的User-Agent，随机选取了User-Agent

   要使之生效需要在 settings.py 中取消DOWNLOADER_MIDDLEWARES注释，并改写成如下内容

   ```python
   DOWNLOADER_MIDDLEWARES = {
      'images360.middlewares.RandomUserAgentMiddleware': 543,
   }
   ```



### Item Pipeline 的用法

1. **作用位置**

   它的调用发生在Spider产生Item之后。当Spider解析完Response之后，Item就会传递到Item Pipeline ,被定义的Item Pipeline的组件会顺次调用，完成一连串处理。

2. **主要功能**

   清理HTML数据

   验证爬取数据，检查爬取字段

   查重并丢弃重复内容

   将爬取结果保存到数据库

3. **核心方法**

   **process_item(item, spider)** 必须要实现的方法



   item：是Item对象，被处理的Item

   spider：生成该Item的Spider



   返回类型

   1.Item 对象，那么此Item会被更低级的Item Pipeline的process_item()方法处理，直到所有的方法都处理完

   2.抛出DropItem异常，那么此Item丢弃，不再进行处理

   其他方法

   open_spider(spider) ：Spider开启的时候自动调用，如打开数据库连接

   close_spider(spider)：Spider关闭的时候自动调用，如关闭数据库

   from_crawler(cls，spider)：

   这是一个类方法，用@classmethod 标识，参数是crawler，通过此对象我们可以拿到Scrapy的所有核心组件，如全局配置的每个信息，然后创建一个Pipeline实例

4. **举例** （存入MySQL数据库）

   在settings.py 中添加几个变量

   ```python
   # 连接数据时需要的参数
   MYSQL_HOST = 'localhost'
   MYSQL_DATABASE = 'spiders'
   MYSQL_PORT = 3306
   MYSQL_USER = 'root'
   MYSQL_PASSWORD = 'yellowkk'#密码
   ```

   实现 MysqlPipeline 在pipelines.py

   ```python
   class MysqlPipeline():
       def __init__(self, host, database, user, password, port):
           self.host = host
           self.database = database
           self.user = user
           self.password = password
           self.port = port
   
       @classmethod
       def from_crawler(cls, crawler):  # 类方法，参数是crawler，通过此对象我们可以拿到Scrapy的所有核心组件
           return cls(
               host=crawler.settings.get('MYSQL_HOST'),
               database=crawler.settings.get('MYSQL_DATABASE'),
               user=crawler.settings.get('MYSQL_USER'),
               password=crawler.settings.get('MYSQL_PASSWORD'),
               port=crawler.settings.get('MYSQL_PORT')
           )
   
       def open_spider(self, spider):
           self.db = pymysql.connect(host=self.host, user=self.user, password=self.password, port=self.port,
                                     db=self.database, charset='utf8')
           self.cursor = self.db.cursor()
   
       def close_spider(self, spider):
           self.db.close()
   
       def process_item(self, item, spider):
           data = dict(item)  # item是一个类字典的类型，将其转化为字典类型、
           keys = ','.join(data.keys())
           values = ','.join(['%s'] * len(data))
           sql = 'insert into image360({}) values({})'.format(keys, values)#插入方法是一个动态构造SQL语句的方法
           self.cursor.execute(sql, tuple(data.values()))
           self.db.commit()
           return item
   ```

   最后在 settings.py 中 设置ITEM_PIPELINES,如下

   ```python
   ITEM_PIPELINES = {
      'images360.pipelines.MysqlPipeline': 300,
   
   }
   ```



-----------------------------------------------------------------------------------------------------------------------------------------------------------