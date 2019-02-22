#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
from mongoengine import *
import scrapy
import datetime
import time
import sqlite3,time
import random
from chardet import detect
from scrapy import log
# from SendPost import insert_post
# from SendPostTopic import insert_posttopic
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
import gridfs
from bson.objectid import ObjectId
# from qsinghua.models import *
import traceback
import pymongo


conn=pymongo.MongoClient('127.0.0.1',27017)
db = conn.wwf_database02
myset = db.kanzheli

# class QsinghuaPipeline(object):
#     def __init__(self):
#         self.items = {
#             "url": "",
#             "site_id": "",
#             "site_name": "",
#             "topic_id": 0,
#             "board": "",
#             "data_type": 1,
#             "title": "",
#             "content": "",
#             "html": "",
#             "img_url": "",
#             "pt_time": "",
#             "st_time": "",
#             "poster":{
#                 "id": "",
#                 "name": "",
#                 "home_url": "",
#                 "img_url": ""
#             },
#             "lan_type": 0,
#             "repost_pt_id": "",
#             'provinces_id_list': [],
#         }


#     def process_item(self, item, spider):
#         print ('!!!!!!!!!!!!!111111111111111')
#         obj_id = ObjectId()
#         file_name = spider.name + "-" + str(time.time())
#         self.items["_id"] = obj_id 
#         self.items["url"] = item["url"]
#         self.items["pt_time"] = item["pt_time"]
#         self.items["title"] = item["title"]
#         self.items["site_id"] = item["site_id"]
#         self.items["comm_num"] =  item['comm_num']
#         self.items["poster"]["name"] = item["poster_name"]
#         self.items["content"] = item["content"]


#         poster = Poster(home_url=self.items['poster']['home_url'],
#                 img_url=self.items['poster']['img_url'],
#                 id=self.items['poster']['id'],
#                 name=self.items['poster']['name']
#         )  

#         #帖子归属话题
#         content = item["title"] + item["content"]

#         topicid = 0
#         topic_kwds_list = []
#         topic_list = []
#         users_list = []
        
#         try:
#             # 添加与或非逻辑
#             i = -1 
#             t = -1
#             topic_obj = Site_topic.objects(site_id=item['site_id'])
#             for obj in topic_obj :
#                 topic_kws = obj.topic_kw
#                 topicid = obj.topic_id
#                 for titem in topic_kws :
#                     for each in titem :
#                         if each in content:
#                             topic_kwds_list.append(each)                        
#                             i = 1
#                             # t = 1
#                         else :
#                             i = -1
#                             break
#                     if i==1 :
#                         t = 1
#                         i = -1 
#                         topic_list.append(topicid)


#             users = User.objects()
#             for user in users:
#                 user_tws = set(user.topic_kws)
#                 post_tws = set(topic_kwds_list)
#                 if len(user_tws & post_tws) > 0:
#                     users_list.append(user.user_id)                    
            
#             post = Post(
#             	_id=self.items['_id'],
#                  url=self.items['url'],
#                  site_id=self.items['site_id'],
#                  site_name=self.items['site_name'],
#                  topic_id = topic_list,
#                  board=self.items['board'],
#                  data_type=self.items['data_type'],
#                  title=self.items['title'],
#                  content=self.items['content'][:500], 
#                  html=' ',
#                  pt_time=self.items['pt_time'],
#                  st_time=datetime.datetime.now,
#                  comm_num=self.items['comm_num'],
#                  topic_kwds = list(set(topic_kwds_list)),
#                  user_id_list = users_list,
#                  img_url=self.items['img_url'],
#                  poster=poster,
#                  provinces_id_list = self.items['provinces_id_list']
#             )
#             post.save()
#             if (t != 1):
#                 pass
#             else:
#                 try:
#                     post.save()
#                     print ("------- insert one ----------")
#         # except NotUniqueError,e:
#         #     Post.objects(site_id=post.site_id, url=post.url).modify(upsert=True, new=True, set__pt_time=post.pt_time)
#         #     print 'updating ...'
#                 except:
#                     # traceback.print_exc()
#                     print ("------- insert failed ----------")

#         except:
#         	# print('oooooooooooo?')
#             traceback.print_exc()
#             # pass

class ElasticsearchPipline(object):
    def process_item(self, item, spider):
    	myset.insert({'user_name':item['poster_name'],
    		'user_gender':item['poster_sex'],'url':item['url'],
    		'content':item['content']})
        item.save_to_es()
        return item
