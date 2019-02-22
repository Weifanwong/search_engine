# -*- encoding: utf-8 -*-
import sys
import json
from elasticsearch import Elasticsearch
from mongoengine import *
import pymongo


conn=pymongo.MongoClient('202.117.43.207',27017)
db = conn.wwf_database02
myset = db.searchresult
# sys.setdefaultencoding("utf8")
 
######################################################
# 用于连接ES环境，查询检索小区信息，返回排名靠前10的小区信息。
# http_auth=('es_username', 'es_passwd')
# es_search(city,name):es_search(深圳,登科花园)
######################################################
 
 
es = Elasticsearch(
        # ['127.0.0.1'],
        # port=9200
)
 
 
def save_result(result_list):
  for i in range(0,len(result_list)):
    print(result_list[i]['_source']['url'])
    myset.insert({'id':i,'url':result_list[i]['_source']['url'],'title':result_list[i]['_source']['title'],
        'content':result_list[i]['_source']['job_desc'],'pt_time':result_list[i]['_source']['crawl_time'],
        'gender':result_list[i]['_source']['gender'],})



def es_search(content):
    query_json = {
            "match": {
              "title": content
            }
        }
 
    source_arr = ["url",
                  "title",
                  "crawl_time",
                  "job_desc",
                  "gender",
                  ]
 
 
 
    res = es.search(index="company",doc_type="d1oc",body={"query": query_json, "_source": source_arr,"size":100},size=100)  # 获取所有数据
 
    # 获取第一条数据，得分最高。
    top_10_recodes = res['hits']['hits']
    # print json.dumps(top_10_recodes)
    # print (top_10_recodes[0]['_source']['url'])
    return top_10_recodes
    #
    # for item in best_recode:
    #     if item != '_source':
    #         print item,best_recode[item]
 
 
# if __name__ == "__main__":
    # 测试单例
    # result_list = es_search('清华大学')
    # save_result(result_list)