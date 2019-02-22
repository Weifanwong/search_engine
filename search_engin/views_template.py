from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date, timedelta
import datetime
from rest_framework.views import APIView
import traceback
import random
#import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
import base64,re
# from yqdata.Auths import *
from django.http import HttpResponse
import random

from mongoengine import *
import json
from mongoengine.queryset.visitor import Q
# from serializers import PostSerializer
from collections import *
import logging
import pymongo

import sys
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

# from flask import Flask, request

# from flask_json import FlaskJSON, as_json_p

# app = Flask(__name__)
# json = FlaskJSON(app)







conn=pymongo.MongoClient('127.0.0.1',27017)
db = conn.wwf_database02
myset = db.searchresult
# sys.setdefaultencoding("utf8")
 
######################################################
# 用于连接ES环境，查询检索小区信息，返回排名靠前10的小区信息。
# http_auth=('es_username', 'es_passwd')
# es_search(city,name):es_search(深圳,登科花园)
######################################################
 

es = Elasticsearch(
        ['127.0.0.1'],
        # http_auth=('elastic', 'passwd'),
        port=9200
)
s = Search(using=es, index="my-index")


logger = logging.getLogger('django')
client = pymongo.MongoClient('127.0.0.1',27017)
db = client['wwf_database02']
table = db['searchresult']
# connect('yuqing', alias='default', host='118.190.133.203', port=27016,username='yuqing',password='yuqing@2017')
connect('wwf_database02',alias='default',host='127.0.0.1',port=27017)



class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)



class Homework_Get_Show(APIView):   #利用get查找
    @csrf_exempt

    def get(self, request, format=None):
        
        search_content=str(request.GET['search'])
        query_json = {
            "match_phrase": {
              "title": search_content
            }
        }

        highlight = {
            "fields" : {
            "title" : {}
        }
        }

        source_arr = ["url",
                      "title",
                      "crawl_time",
                      "job_desc",
                      "gender",
                      ]
 
        # res = s.query("match",title=search_content).execute()
        res = es.search(index="my-index",doc_type="doc",body={"query": query_json, "_source": source_arr,"highlight":highlight},size=100)  # 获取所有数据

     
 
    # 获取第一条数据，得分最高。
        result_list = res['hits']['hits']
        # print(result_list)
        show_table=[]
        json_out={}
        try:
            for item in result_list:
                content = item['_source']['job_desc'].strip('<p>').strip('<br>').strip('</font>')
                show_table.append({'url':item['_source']['url'],'title':item['_source']['title'],'content':content})
                # ,'content':item['_source']['job_desc'] 
            json_out={"Show":"Success"}
        except:
            json_out={"Show":"no such id"}
        # print(show_table)
        # print(type(json.loads(json_out,cls=MyEncoder,ensure_ascii=False)))
        #return HttpResponse(tmp[0]['topic_name'])#tmp存放的是多个topic_template组成的数组，而new_obj存放的是topic_template类型
        print(show_table)
        return HttpResponse(json.dumps(show_table, cls=MyEncoder,ensure_ascii=False),content_type="application/json")
        #return HttpResponse(json_out)
        ##question:1、“查”究竟是将数据显示到哪里接收符合条件的数据的时候必须用这种json数据类型来吗？有没有其他办法？

    

class Homework_Post_Show(APIView):    #利用post增加
    @csrf_exempt #这一行干啥的
    def post(self,request,format=None):
        json_out = {}

        try:
            json_data = request.data
            json_out={"Show":"Success"}
        except:
            json_out={"Show":"no such id"}

        #json_out={}
        json_data = request.data
        
        return HttpResponse(json.dumps(json_data, cls=MyEncoder),content_type="application/json")






