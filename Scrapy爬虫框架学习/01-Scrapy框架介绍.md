# Scrapy 框架学习
### 一、Scrapy 框架介绍

	Scrapy不是一个函数功能库，而是一个**爬虫框架**
	什么是爬虫框架？
	爬虫框架是实现爬虫功能的一个软件结构和功能组件集合。
	爬虫框架是一个半成品，能够帮助用户实现专业网络爬虫

### 1.架构介绍

![image](https://github.com/YilK/Web-Crawler/blob/master/Scrapy%E7%88%AC%E8%99%AB%E6%A1%86%E6%9E%B6%E5%AD%A6%E4%B9%A0/1.png)


**Scrapy Engine**

	引擎负责控制数据流在系统中所有组件中流动，并在相应动作发生时触发事件。详细内容查看下面的数据流(Data Flow)部分
此组件相当于爬虫的“大脑”，是整个爬虫的调度中心。

**Scheduler(调度器)**

	调度器从引擎接受request并将他们入队，以便之后引擎请求他们时提供给引擎。
初始的爬取URL和后续在页面中获取的待爬取的URL将放入调度器中，等待爬取。同时调度器会自动去除重复的URL（如果特定的URL不需要去重也可以通过设置实现，如post请求的URL）

**Downloader(下载器)**

	下载器负责获取页面数据并提供给引擎，而后提供给spider。

**Spider**
​	
	Spider是Scrapy用户编写用于分析response并提取item(即获取到的item)或额外跟进的URL的类。 每个spider负责处理一个特定(或一些)网站。 

**Item Pipeline**

	Item Pipeline负责处理被spider提取出来的item。典型的处理有清理、 验证及持久化(例如存取到数据库中
当页面被爬虫解析所需的数据存入Item后，将被发送到项目管道(Pipeline)，并经过几个特定的次序处理数据，最后存入本地文件或存入数据库。

**Downloader middleware(下载器中间键)**

	下载器中间件是在引擎及下载器之间的特定钩子(specific hook)，处理Downloader传递给引擎的response。 其提供了一个简便的机制，通过插入自定义代码来扩展Scrapy功能。
通过设置下载器中间件可以实现爬虫自动更换user-agent、IP等功能。

**Spider middleware(Spider中间件)**

	Spider中间件是在引擎及Spider之间的特定钩子(specific hook)，处理spider的输入(response)和输出(items及requests)。 其提供了一个简便的机制，通过插入自定义代码来扩展Scrapy功能。

### 2.数据流


       1.引擎打开一个网站(open a domain)，找到处理该网站的Spider并向该spider请求第一个要爬取的URL(s)。
    
       2.引擎从Spider中获取到第一个要爬取的URL并在调度器(Scheduler)以Request调度。
    
       3.引擎向调度器请求下一个要爬取的URL。
    
       4.调度器返回下一个要爬取的URL给引擎，引擎将URL通过下载中间件(请求(request)方向)转发给下载器(Downloader)。
    
       5.一旦页面下载完毕，下载器生成一个该页面的Response，并将其通过下载中间件(返回(response)方向)发送给引擎。
    
       6.引擎从下载器中接收到Response并通过Spider中间件(输入方向)发送给Spider处理。
    
       7.Spider处理Response并返回爬取到的Item及(跟进的)新的Request给引擎。
    
       8.引擎将(Spider返回的)爬取到的Item给Item Pipeline，将(Spider返回的)Request给调度器。
    
       9.(从第二步)重复直到调度器中没有更多地request，引擎关闭该网站。


### 3.创建项目
它是通过**命令行**来创建项目的，代码的编写还是需要通过IDE
​	

``` 
scrapy startproject scrapyspider
```
项目创建之后文件结构

``` 
scrapyspider/
    scrapy.cfg
    scrapyspider/
        __init__.py
        items.py
        pipelines.py
        settings.py
        middlewares.py
        spiders/
            __init__.py
            ...
```
各文件的功能描述

	1.scrapy.cfg：Scrapy项目的配置文件
	2.tutorial/: 该项目的python模块。之后您将在此加入代码。
	3.tutorial/items.py: 项目中的item文件。
	4.tutorial/pipelines.py: 项目中的pipelines文件。
	5.tutorial/settings.py: 项目的设置文件。
	6.tutorial/middlewares.py:	定义Spider Middlewares和Downloader Middlewares的实现
	6.tutorial/spiders/: 放置spider代码的目录


### 四、其他

#### 1.Scrapy爬虫的使用步骤
==1.创建一个工程和Spider模板==	
``` 
创建项目：scrapy startproject tutorial
创建Spider：cd turorial
					  scrapy genspider qutoes qutoes.toscrape.com
```
==2.编写Spider==
==3.编写Item Pipeline==
==4.优化配置策略==

#### 2.Scrapy爬虫的数据类型
Request 类
Response 类
Item 类

(1)Request 类

	a.Request对象表示一个HTTP请求
	b.由Spider生成，由Downloader执行


|  属性或方法  |   说明  |
| ---| ---|
|.url|Request对应的请求URL地址        |
|.method|对应的请求方法，'GET''POST'等    |
|.headers|字典类型风格的请求头    |
|.body|请求内容主体，字符串类型     |
|.meta|用户添加的扩展信息，在Scrapy内部模块间传递信息使用.copy()复制该请求  |
|.copy()|复制该请求    |

(2)Response 类
​	
	a.Response对象表示一个HTTP响应 
	b.由Downloader生成，由Spider处理
|  属性或方法  |   说明  |
| ---| ---|
|.url|Request对应的请求URL地址        |
|.status|HTTP状态码，默认是200    |
|.headers|Response对应的头部信息    |
|.flags|一组标记|
|.body|请求内容主体，字符串类型     |
|.request|产生Response类型对应的Request对象  |
|.copy()|复制该响应|

(3)Item 类

	a.Item对象表示一个从HTML页面中提取的信息内容 
	b.由Spider生成，由Item Pipeline处理 
	c.Item类似字典类型，可以按照字典类型操作



 
