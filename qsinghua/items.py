# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
# from qsinghua.models import ShuiMuType
from qsinghua.es_operation import ShuimuType
from elasticsearch_dsl.connections import connections
es = connections.create_connection(hosts=['127.0.0.1'])



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
    def save_to_es(self):
        shuimu_type=ShuimuType()
        shuimu_type.url=self["url"]
        shuimu_type.title=self["title"]
        shuimu_type.job_desc=self['content']
        shuimu_type.crawl_time=self['pt_time']
        shuimu_type.gender=self['poster_sex']
        shuimu_type.save()
        return