# -*- coding: utf-8 -*-
import scrapy
from images360.settings import MAX_PAGE
from images360.items import Images360Item
import json


class ImagesSpider(scrapy.Spider):
    name = 'images'
    '''
    这里将start_urls 列表删去了
    start_urls: 它是起始URL列表，当我们没有实现start_requests()方法时，默认会从这个列表开始抓取
    '''

    def start_requests(self):  # 此方法用于生成初始请求，它必须返回一个可迭代对象
        for page in range(MAX_PAGE):  # MAX_PAGE在settings.py中定义好了
            url = 'https://images.so.com/zj?ch=photography&sn={}&listtype=new&temp=1'.format(page * 30)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        result = json.loads(response.body)
        item = Images360Item()
        for image in result.get('list'):  # 遍历一个列表
            item['id'] = image.get('imageid')  # ID
            item['url'] = image.get('qhimg_url')  # url
            item['title'] = image.get('group_title')  #标题
            yield item

