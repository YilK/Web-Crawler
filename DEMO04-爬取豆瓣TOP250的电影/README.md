此次对豆瓣TOP250的电影进行了爬取

要添加请求头User-Agent，否则访问不了

在settings.py 中添加了`USER_AGENT='Mozilla/5.0'`

[DoubanMovieTOP250.csv](https://github.com/YilK/Web-Crawler/blob/master/DEMO04-%E7%88%AC%E5%8F%96%E8%B1%86%E7%93%A3TOP250%E7%9A%84%E7%94%B5%E5%BD%B1/DoubanMovieTOP250.csv) 是爬取的结果

**出现的问题：**

执行 `scrapy crawl DoubanMovieTOP250 -o DoubanMovieTOP250.csv`

打开csv文件，会发现出现很多奇怪的字体。

**解决办法：**

使用Notepad++打开，改变编码格式为：UTF-8-BOM