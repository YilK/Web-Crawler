# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanmovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #排名
    ranking=scrapy.Field()
    #电影名称
    movie_name=scrapy.Field()
    #电影的得分
    score=scrapy.Field()
    #经典的影评
    review=scrapy.Field()