# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import QuoteItem

class QutoesSpider(scrapy.Spider):
    name = 'qutoes'
    # allowed_domains = ['qutoes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        #利用CSS选择器
        quotes=response.css('.quote')#找到存储着有效信息的标签
        for quote in quotes:#遍历标签
            item=QuoteItem()
            item['text']=quote.css('.text::text').extract_first()
            item['author']=quote.css('.author::text').extract_first()
            item['tags']=quote.css('.tags .tag::text').extract()
            yield item#将item返回
            next=response.css('.pager .next a::attr("href")').extract_first()
            url='http://quotes.toscrape.com'+str(next)
            yield scrapy.Request(url=url,callback=self.parse)#callback：回调函数
            #将该url对应的响应作为参数传递给回调函数