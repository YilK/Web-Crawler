# Scrapy入门

## 学习的内容：

1. 创建Scrapy项目。
2. 创建一个Spider来抓取站点和处理数据。
3. 通过命令行将抓取的内容导出。

### 1.创建项目

​	终端输入

​	`scrapy startproject tutorial`

​	建立了一个名为turorial的文件夹

​	文件夹结构

​	turorial/
   		scrapy.cfg	#Scrapy部署时的配置文件
​    		turorial/		#项目模块
​        		\____init\____.py		
​        		items.py		#Items的定义，定义爬取的数据结构
​       	 		pipelines.py		#Pipelines的定义，定义数据管道	
​        		settings.py		#定义Spider Middlewares和Downloader Middlewares的实现
​        		spiders/		#放置Spiders的文件夹
​           			\____init\____.py	

### 2.创建Spider

​	`cd tutorial	`	#进入文件夹

​	`scrapy genspider qutoes qutoes.toscrape.com`	#执行genspider命令，第一个参数是spider的名称，第二个参数是网站的域名

​	执行完，spiders文件夹中多了一个qutoes.py

​	

```python
# -*- coding: utf-8 -*-
import scrapy

class QutoesSpider(scrapy.Spider):
    name = 'qutoes'	
    # allowed_domains = ['qutoes.toscrape.com']  
    start_urls = ['http://quotes.toscrape.com/']
    
    def parse(self, response):
        pass
```

​	**name**：定义spider名字的字符串(string)。是必须的

​	**allowed_domains**：可选。包含了spider允许爬取的域名(domain)列表(list)。 当 OffsiteMiddleware 启用						  时， 域名不在列表中的URL不会被跟进。

​	**start_urls**：URL列表。当没有制定特定的URL时，spider将从该列表中开始进行爬取。 因此，第一个被获取到的页面的URL将是该列表之一。 后续的URL将会从获取到的数据中提取。

​	**parse**：当response没有指定回调函数时，该方法是Scrapy处理下载的response的默认方法。



### 3.创建Item

​	什么是Item？

​		官方定义：

​			爬取的主要目标就是从非结构性的数据源提取结构性数据，例如网页。 Scrapy spider可以以python的dict来返回提取的数据.虽然dict很方便，并且用起来也熟悉，但是其缺少结构性，容易打错字段的名字或者返回不一致的数据，尤其在具有多个spider的大项目中。。

为了定义常用的输出数据，Scrapy提供了 [`Item`](https://scrapy-chs.readthedocs.io/zh_CN/1.0/topics/items.html#scrapy.item.Item) 类。 [`Item`](https://scrapy-chs.readthedocs.io/zh_CN/1.0/topics/items.html#scrapy.item.Item) 对象是种简单的容器，保存了爬取到得数据。 其提供了 [类似于词典(dictionary-like)](https://docs.python.org/library/stdtypes.html#dict) 的API以及用于声明可用字段的简单语法。

许多Scrapy组件使用了Item提供的额外信息: exporter根据Item声明的字段来导出数据、 序列化可以通过Item字段的元数据(metadata)来定义、 `trackref` 追踪Item实例来帮助寻找内存泄露 (see [使用 trackref 调试内存泄露](https://scrapy-chs.readthedocs.io/zh_CN/1.0/topics/leaks.html#topics-leaks-trackrefs)) 等等。



​	简单的来说：

​	Item是保存爬取数据的容器，它的使用方法和字典类似。不过和字典相比，Item多了额外的保护机制，可以	避免拼写错误或者定义字段错误

​	

​	创建item需要继承scarpy.Item类，并且定义类型为scrapy.Field的字段，观察目标网站，网可以获取到的内容有text，author，tags。

​	修改item.py 如下

​		

```python
import scrapy


class  QuoteItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()

```



​		

### 4.解析Response

​	parse()方法的参数response是start_urls里面链接爬取后的结果。所以在parse()中我们可以直接对response中包含的内容进行解析

​	提取的内容方式有多种，下面使用**CSS选择器**

​	

```python
    def parse(self, response):
        #利用CSS选择器
        quotes=response.css('.quote')#找到存储着有效信息的标签
        for quote in quotes:#遍历标签
            text=quote.css('.text::text').extract_first()#提取内容
            author=quote.css('.author::text').extract_first()
            tags=quote.css('.tags .tag::text').extract()
```

这里需要注意的几个点

`response.css('.quote')`	#返回的是一个SelectorList 对象 

```
SelectorList 类是内建 list 类的子类，提供了一些额外的方法:

xpath(query)	#寻找可以匹配xpath query 的节点，并返回 SelectorList 的一个实例结果，单一化其所有元素。列表元素也实现了 Selector 的接口。

css(query)		#应用给定的CSS选择器，返回 SelectorList 的一个实例。
query 是一个包含CSS选择器的字符串。

extract()		#串行化并将匹配到的节点返回一个unicode字符串列表
extract_first()#获得第一个元素
还有其他一些方法
https://scrapy-chs.readthedocs.io/zh_CN/1.0/topics/selectors.html
```



### 5.使用Item

​	Item可以理解为一个字典，不过在声明的时候需要实例化。然后依次用刚才解析的结果赋值Item的每一个字段，最后将Item返回。

​	改写parse()

```python
    def parse(self, response):
        #利用CSS选择器
        quotes=response.css('.quote')#找到存储着有效信息的标签
        for quote in quotes:#遍历标签
            item=QuoteItem()
            item['text']=quote.css('.text::text').extract_first()
            item['author']=quote.css('.author::text').extract_first()
            item['tags']=quote.css('.tags .tag::text').extract()
            yield item#将item返回
```



### 6.后续的Request

​	以上的操作只能爬取第一页，我们也需要爬取后面几页。

​	<u>所以我们需要在页面中找到信息来生成下一个请求</u>

​	查看源代码，可以发现链接是 /page/2/，

​	通过这个链接我们构造下一个请求

```python
    def parse(self, response):
        #利用CSS选择器
        quotes=response.css('.quote')#找到存储着有效信息的标签
        for quote in quotes:#遍历标签
            item=QuoteItem()
            item['text']=quote.css('.text::text').extract_first()
            item['author']=quote.css('.author::text').extract_first()
            item['tags']=quote.css('.tags .tag::text').extract()
            yield item#将item返回
            #构造下一个请求
            next=response.css('.pager .next a::attr("href")').extract_first()
            url='http://quotes.toscrape.com'+str(next)
            yield scrapy.Request(url=url,callback=self.parse)#callback：回调函数
            #将该url对应的响应作为参数传递给回调函数
```

​	

​	构造时需要用到 scrapy.Request。这里还需要传递两个参数---**url**和**callback**

​	**url**：指请求链接

​	**callback**：指回调函数，将url对应的响应作为参数传递给回调参数



### 7.运行并保存

​	`scarpy crawl quotes -o quotes.csv`		#保存为csv格式文件

​	`scarpy crawl quotes -o quotes.json`	#保存为JSON文件

​	。。。。。还有其他格式的