

# Scrapy对接Selenium爬取京东商品

**前面学习使用Selenium爬取京东的商品，这一次使用Scrapy对接Selenium的方式来爬取京东的商品**

## 步骤

### 1.新建项目、新建Spider、修改ROBOTSTXT_OBEY

```
scrapy stratproject scrapyseleniumJD
cd scrapyseleniumJD
scrapy genspider JDproduct www.jd.com
```

在 settings.py 中修改 ROBOTSTXT_OBEY

```python
ROBOTSTXT_OBEY = False  # 不遵守Robots协议
```



### 2.定义Item 

```python
import scrapy
class ScrapyseleniumjdItem(scrapy.Item):
    # 声明Item对象
    img_url = scrapy.Field() # 商品图片的url
    price = scrapy.Field() # 商品的价格
    title = scrapy.Field() # 商品的名称
    shop = scrapy.Field() # 店铺
```

​	定义了 4 个字段



### 3.实现 start_requests()

```python
from urllib.parse import quote
from scrapyseleniumJD.settings import KEYWORD  # 要爬取的商品在settings.py定义，表示要爬取的商品

class JdproductSpider(scrapy.Spider):
    name = 'JDproduct'
    base_url = 'https://search.jd.com/Search?keyword='
    def start_requests(self):  # 生成初始请求
        for page in range(1, 10):  # 爬取此商品页面的第几页
            url = self.base_url + quote(KEYWORD)  # quote()将内容转化为URL的编码格式
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': page}, dont_filter=True)
            '''
            其实这里的每一个url是一样的。
            meta 的作用使用来传递数据的(在这里传递的是页码)，在Download Middleware中会用到这个page。 
            dont_filter=True 表示这个url不参与去重
            '''
```

​	需要注意 ==meta== 与 ==dont_filter== 的用法



#### 4.对接Selenium

​	接下来要处理这些抓取的请求，我们对接Selenium进行抓取，采用 ==Downloader Middleware==来实现

​	编辑自己的下载中间件，在 middlewares.py 中创建

```python
# 编辑自己的下载中间件
class SeleniumMiddleware():
    def __init__(self): # 初始化 
        self.logger = getLogger(__name__)
        self.browser = webdriver.Chrome()  # 声明浏览器对象
        self.browser.set_page_load_timeout(10)  # 设定页面加载设定时间
        self.wait = WebDriverWait(self.browser, 10)  # 显式等待

    def __del__(self):
        self.browser.close()  # 关闭页面

    def process_reqest(self, request, spider):  # 抓取页面
        self.logger.debug('staring !!!!!!!')
        page = request.meta.get('page')  # 获得页码
        try:
            self.browser.get(request.url)  # 访问初始页面
            for i in range(1, 3):  # 将页面拖拽到底部，页面全部加载出来，不然后面找不到其他页面的信息
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
            if page > 1:
                input = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'span input.input-txt')))  # 直到节点加载出来
                button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.p-skip a')))  # 直到该节点可点击
                input.clear()  # 清除节点里内容
                input.send_keys(page)  # 输入要到达的页面
                button.click()  # 点击确定按钮
                # 判断是否是当前的页码
            self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'span.p-num a.curr'), str(page)))
            self.browser.execute_script("window.scrollBy(0, 5000)")  # 滑倒页面中部，等待2s，加载剩余的商品信息
            # self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  ，到页面的底部应该也可以，但是我没尝试
            time.sleep(2)
            # 返回Response的子类对象，会直接将Response对象交给Spier处理
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',status=200)

        except:
            return HtmlResponse(url=request.url, status=500, request=request)
```

​	里面部分代码是从上次上传的代码中粘贴

​	[**利用Selenium爬取京东商品.py**](https://github.com/YilK/Web-Crawler/blob/master/DEMO07-%E5%88%A9%E7%94%A8Selenium%E7%88%AC%E5%8F%96%E4%BA%AC%E4%B8%9C%E5%95%86%E5%93%81/%E5%88%A9%E7%94%A8Selenium%E7%88%AC%E5%8F%96%E4%BA%AC%E4%B8%9C%E5%95%86%E5%93%81.py)

​	需要注意的是：在 ==process_reqest(self, request, spider)== 中返回的是一个Response对象 ，返回了Response对象，它会被直接发送给Spider，不再使用Scrapy中的 Downloader

​	当 process_request() 返回 Response 对象，Scrapy将不会调用任何其他的 process_request() 或process_exception() 方法，或相应地下载函数；转而开始执行每个 Downloader Middleware 的 process_response() 方法，调用完毕之后直接将Response对象发送给 Spider 处理 

然后在 settings.py 中设置

```python
DOWNLOADER_MIDDLEWARES = {
   'scrapyseleniumJD.middlewares.SeleniumMiddleware': 543,
}
```



### 5.解析页面

```PYTHON
def parse(self, response):
    products = response.css('li.gl-item')
    for product in products:  # 找到需要的信息
        item = ScrapyseleniumjdItem()
        # 利用正则表达式匹配出图片的url
        match = re.search(r'//(.*g)', product.css('a[target="_blank"] img').extract_first(),re.S)
        if match:
            item['img_url'] = match.group(1)
        else:
            item['img_url'] = product.css('a[target="_blank"] img').extract_first()

        item['title'] = product.css('div.p-name a::attr(title)').extract_first()
        item['price'] = product.css('div div.p-price strong i::text').extract_first()
        item['shop'] = product.css('div.p-shop span a::attr(title)').extract_first()
        yield item
```



### 6.存储结果

在 pipelines.py 中定义

```python
# 存入MongoDB
class MongoPipeline(object):
    def __init__(self):
        self.MONGO_URL = 'localhost'
        self.MONGO_DB = 'test'
        self.MONGO_COLLECTION = 'JDproducts__fix'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host=self.MONGO_URL)  # 连接到MongoDB
        self.db = self.client[self.MONGO_DB]  # 指定数据库

    def process_item(self, item, spider):
        collection = self.db[self.MONGO_COLLECTION]  # 指定集合
        collection.insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()  # 关闭
```

在 settings.py 中设置

```python
ITEM_PIPELINES = {
   'scrapyseleniumJD.pipelines.MongoPipeline': 300,
}
```



### 7.最后

scrapy crawl JDproduct



# 出现的问题

我发现一页只能爬取到30个商品的信息，没有将60个商品全部爬取下来。。。但是不用Scrapy就可以爬取到所有的商品。。。。。。。难受。。。。。。。