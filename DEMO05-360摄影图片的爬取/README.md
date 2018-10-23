这一次爬取了360的摄影图片，没将其下载下来，只是保存了url及其他信息。

这一次学习到， **修改User-Agent** ，并将数据存入了**数据库**。

#### 修改User-Agent

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



#### 将数据存入数据库

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

