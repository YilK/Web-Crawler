# -*- coding: utf-8 -*-
import scrapy
from DoubanMovie.items import DoubanmovieItem


class Doubanmovietop250Spider(scrapy.Spider):
    name = 'DoubanMovieTOP250'
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        movies = response.css('ol.grid_view li')  # 利用CSS选择器找到存储着信息的标签,由Selector对象组成的列表
        for movie in movies:
            item = DoubanmovieItem()  # 声明Item
            item['ranking'] = movie.css('em::text').extract_first()  # 排名信息
            item['movie_name'] = movie.css('a img::attr(alt)').extract_first()  # 电影的名称
            item['score'] = movie.css('.rating_num::text').extract_first()  # 得分
            item['review'] = movie.css('.inq::text').extract_first()  # 影评
            yield item
        # 翻页
        url = response.css('span.next a::attr(href)').extract_first()  # url
        if url:
            next_url = 'https://movie.douban.com/top250' + url  # 后一页
            yield scrapy.Request(url=next_url, callback=self.parse)  # 回调函数
