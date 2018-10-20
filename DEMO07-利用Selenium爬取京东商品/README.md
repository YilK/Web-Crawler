# 使用Selenium爬取京东商品

以前写过使用Selenium爬取淘宝的商品，但是现在爬取淘宝需要登录，Cookies也获取不到，使用Selenium也登录不了。所以现在尝试爬取京东的商品



## 要点：

### 1.使用显式等待

```python
wait = WebDriverWait(browser, 10)  # 显式等待，指定最长等待时间为10s
```

### 2.拖拽页面

​	1.第一次拖拽操作

​	我设置的翻页是将==指定的页码输入==然后点击==确定按钮==进行翻页，所以需将输入页码的节点与确定按钮给加载出来。

所以**拖拽页面到底部**，将需要的节点加载出来

```python
for i in range(1, 3):  
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
```

​	2.第二次拖拽操作

​	第一次拖拽操作完成，模拟输入页码，点击确定，到达指定页。

​	到达指定页后不将页面下拉只能获取到30个商品的信息，将页面下拉之后还能够获取到其他30个商品信息（就是将所有的商品信息加载出来）。所以还需要模拟拖拽操作​	

```python
browser.execute_script("window.scrollBy(0, 5000)")  # 滑倒页面中部，等待2s，加载信息
time.sleep(2)
```

​	

### 3.解析页面，获取商品的信息

​	我使用了使用 Scrapy 提供的 Selector 来解析

```python
from scrapy import Selector
html = browser.page_source  # 获取页面的源代码
selector = Selector(text=html)  # 使用Scrapy提供的Selector来解析
```

​	利用 css 选择器来提取自己想要的信息

​	**提取图片的 url 时出现的问题**

​	图片的url 会在标签属性 src 或 data-lazy-img 下  所以只能先找到标签，然后利用正则表达式提取出url

​	这是我的想法，在代码里没写。。。。。。。。

### 4.将数据存入MongoDB

​	这个很简单。。。

