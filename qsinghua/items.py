# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShuiMuPostItem(scrapy.Item):
    url = scrapy.Field() #
    site_name = scrapy.Field() #
    title = scrapy.Field() #
    content = scrapy.Field()#
    pt_time = scrapy.Field()
    poster_name = scrapy.Field()#
    comm_num = scrapy.Field()#
    img_url = scrapy.Field()#
    poster_num = scrapy.Field()#
    poster_sex = scrapy.Field()
    site_id = scrapy.Field()

