# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import quote
from scrapyseleniumJD.settings import KEYWORD  # 要爬取的商品在settings.py定义
from scrapyseleniumJD.items import ScrapyseleniumjdItem
import re


class JdproductSpider(scrapy.Spider):
    name = 'JDproduct'
    base_url = 'https://search.jd.com/Search?keyword='
    def start_requests(self):  # 生成初始请求
        for page in range(1, 10):  # 爬取此商品页面的第几页
            url = self.base_url + quote(KEYWORD)  # quote()将内容转化为URL的编码格式
            yield scrapy.Request(url=url, callback=self.parse, meta={'page': page}, dont_filter=True)
            '''
            其实这里的每一个url是一样的，meta的作用使用来传递数据的(传递的是要到达的页数)在Download Middleware中
            会用到这个page，dont_filter=True 表示这个url不参与去重
            '''

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
