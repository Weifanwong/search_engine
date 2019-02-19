# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 chaoqiankeji.com, Inc. All Rights Reserved
#

"""
File: models.py
Author: minus(minus@stu.xjtu.edu.cn)
Date: 2016-12-26 12:36
Project: TestPy
"""
import mongoengine
from mongoengine import *
from mongoengine.context_managers import switch_db
import datetime
from datetime import datetime

from elasticsearch_dsl import DocType, Date, Nested, Boolean,analyzer, InnerDoc, Completion, Keyword, Text, Integer

from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=["localhost"])

DATA_TYPE = (0, 1, 2, 3, 4, 5, 6)
IS_RUN = (0, 1)

# meta = {
#     'shard_key': ('machine', 'timestamp',)
# }

# class Page(Document):
#     title = StringField(max_length=200, required=True)
#     pt_time = DateTimeField(default=datetime.datetime.now)
#     html = FileField()
#     meta = {'collection': 'page'}

class PostQuerySet(QuerySet):

    def get_posts_by_topics(self):
        return self.order_by('topic_id', 'pt_time')

    def get_posts_by_sites(self):
        return self.order_by('site_id', 'pt_time')

    def get_posts_by_sites_topics(self):
        return self.order_by('site_id','topic_id', 'pt_time')

    def get_posts_by_datatype(self, datatype):
        return self(data_type=datatype)

class Datatype_name(Document):
    data_type = IntField(required=True, unique=True)
    datatype_name = StringField(required=True, max_length=16, unique=True)

class Poster(EmbeddedDocument):
    home_url = StringField(max_length=512)
    img_url = StringField(max_length=512)
    id = StringField(max_length=64)
    name = StringField(max_length=64)
    follows = IntField(required=False,unique=False)
    following = IntField(required=False,unique=False)
    post_num = IntField(required=False,unique=False)
    level = StringField(max_length=128)
    location = StringField(max_length=128)
    intro = StringField(max_length=2048)
    birthday = StringField(max_length=128)
    authentication = StringField(max_length=128)
    fan_url = StringField(max_length=512)
    follow_url = StringField(max_length=512)
    abstract = StringField(max_length=128)
    sex = StringField(max_length=64)


class Topic_kw(EmbeddedDocument):
    _and = ListField(StringField(),default=list)
    _or = ListField(StringField(),default=list)


class User(Document):
    _id = ObjectIdField(primary_key=True)
    user_id = IntField(required=True, unique=True)
    user_name = StringField(max_length=64, required=True, unique=True)

    meta = {
        'ordering' : ['user_id'],
        'collection' : 'user',
        'indexes' : [
                'user_id',
                'user_name'
            ]
    }

# class Sen_message(Document):
#     _id = ObjectIdField(primary_key=True)
#     url = StringField(required=True, max_length=512, unique_with='user_id_list')
#     site_id = IntField(required=True)
#     site_name = StringField(max_length=64)
#     # topic_id = IntField(required=False, default=0)
#     topic_id = ListField(IntField(), default=list)
#     board = StringField(max_length=200)
#     data_type = IntField(required=True)
#     title = StringField(max_length=500)
#     content = StringField(max_length=2048)
#     # topic_name = StringField(max_length=512)
#     topic_name = ListField(StringField(), default=list)
#     html = FileField()
#     pt_time = DateTimeField(required=True)
#     st_time = DateTimeField(default=datetime.datetime.now)
#     add_time = DateTimeField(default=datetime.datetime.now)
#     read_num = IntField(default=0)
#     comm_num = IntField(default=0)
#     img_url = StringField(max_length=512)
#     repost_num = IntField(default=0)
#     lan_type = IntField(default=0)
#     repost_pt_id = StringField(required=False)
#     text_type = IntField(required=False)
#     poster = EmbeddedDocumentField(Poster)
#     is_report = IntField(default=0)  # 未上报0 已上报1 已处理2 
#     phone_num = StringField(max_length=20)
#     qq_num = StringField(max_length = 20)
#     ip_addr = StringField(max_length=20)
#     sen_words = ListField(StringField(), default=list)
#     reporter_id = IntField(default=0)
#     reporter_account = StringField(max_length=64)
#     reporter_group_id = IntField(default=1)
#     user_id_list = ListField(IntField(), default=list)
#     geography = StringField(max_length=64)
#     meta = {
#         'ordering': ['-pt_time'],
#         'collection': 'sen_message',
#         'indexes':[
#             'topic_id',
#             'pt_time',
#             ('data_type', 'site_id'),  # 复合index
#         ]
#     }

class Post(Document):
    _id = ObjectIdField(primary_key=True)
    url = StringField(required=True, max_length=512, unique=True)
    site_id = IntField(required=True)
    site_name = StringField(max_length=64)
    # topic_id = IntField(required=False, default=0)
    topic_id = ListField(IntField(), default=list)
    hot_topic_id = IntField(required=False, default=0)
    board = StringField(max_length=200)
    data_type = IntField(required=True, choices=DATA_TYPE)
    title = StringField(max_length=500)
    content = StringField(max_length=2048)
    html = FileField()
    pt_time = DateTimeField(required=True)
    # st_time = DateTimeField(default=datetime.datetime.now)
    read_num = IntField(default=0)
    comm_num = IntField(default=0)
    img_url = StringField(max_length=512)
    repost_num = IntField(default=0)
    lan_type = IntField(default=0)
    is_read = IntField(default=0)
    repost_pt_id = StringField(required=False)
    text_type = IntField(required=False)
    phone_num = StringField(max_length=20)
    qq_num = StringField(max_length = 20)
    ip_addr = StringField(max_length=20)
    poster = EmbeddedDocumentField(Poster)
    topic_kwds = ListField(StringField(),default=list)
    user_id_list = ListField(IntField(), default=list)
    should_pull = BooleanField(required=False,default=False)
    provinces_id_list = ListField(IntField(),default=list)


    meta = {
        'ordering': ['-pt_time'], # 默认的　objects()
        'collection': 'post',
        # 'shard_key': ('site_id', 'topic_id', 'pt_time'),
        'queryset_class': PostQuerySet,
        'indexes':[
            'topic_id',
            'pt_time',
            '$title',   # text index
            ('data_type', 'site_id'),  # 复合index
        ]
    }


class Topic(Document):
    _id = IntField(required=True, primary_key=True)
    topic_name = StringField(required=True, max_length=64)
    topic_kw = ListField(ListField(StringField(), default=list),default=list)
    topic_kws = ListField(StringField(),default=list)
    user_id = IntField(required=True, unique_with='topic_name')
    user_name = StringField(required=True, max_length=32)
    summary = StringField(required=False)

    meta = {
        'ordering': ['_id'],
        'collection': 'topic'
    }




class Hot_Topic(Document):
    _id = IntField(required=True, primary_key=True)
    topic_name = StringField(required=True, max_length=64)
    topic_kws = ListField(StringField(), default=list)
    user_id = IntField(required=True, unique_with='topic_name')
    user_name = StringField(required=True, max_length=32)
    summary = StringField(required=False)   

    meta = {
        'ordering': ['_id'],
        'collection': 'hot_topic'
    }

class Site(Document):
    _id = IntField(required=True, primary_key=True)
    site_name = StringField(required=True, max_length=64, unique_with='_id')
    site_url = URLField(required=True)
    data_type = IntField(required=True, choices=DATA_TYPE)
    position = IntField(default=0)
    is_run = IntField(default=0, choices=IS_RUN)

    meta = {
        'ordering': ['_id'],
        'collection': 'site'
    }

class Site_topic(Document):
    site_id = IntField(required=True)
    topic_id = IntField(required=True)
    topic_name = StringField(required=True, max_length=64)
    topic_kws = ListField(StringField(), default=list)
    user_id = IntField(required=True, unique_with=['site_id', 'topic_id'])
    user_name = StringField(required=True, max_length=32)
    topic_kw = ListField(ListField(StringField(), default=list),default=list)

    meta = {
        'ordering': ['site_id'],
        'collection': 'site_topic'
    }


class Cloud_formain(Document):
    _id = ObjectIdField(primary_key=True)
    word = StringField(max_length=128)
    frequency = IntField(required=False,unique=False)
    topic_id=IntField(required=True)
    sday=DateTimeField(required=True)
    WORD_TYPE=StringField(max_length=128)
    meta = {
    	'collection' : 'cloud_formain'
    }


class Post_News(Document):
    _id = ObjectIdField(primary_key=True)
    url = StringField(required=True, max_length=512, unique=True)
    site_id = IntField(required=True)
    site_name = StringField(max_length=64)
    hot_topic_id = IntField(required=False, default=0)
    board = StringField(max_length=200)
    data_type = IntField(required=True, choices=DATA_TYPE)
    title = StringField(max_length=500)
    content = StringField(max_length=2048)
    html = FileField()
    pt_time = DateTimeField(required=True)
    # st_time = DateTimeField(default=datetime.datetime.now)
    read_num = IntField(default=0)
    comm_num = IntField(default=0)
    img_url = StringField(max_length=512)
    repost_num = IntField(default=0)
    lan_type = IntField(default=0)
    is_read = IntField(default=0)
    repost_pt_id = StringField(required=False)
    text_type = IntField(required=False)
    phone_num = StringField(max_length=20)
    qq_num = StringField(max_length = 20)
    ip_addr = StringField(max_length=20)
    poster = EmbeddedDocumentField(Poster)
    should_pull = BooleanField(required=False,default=False)

    meta = {
        'ordering': ['-pt_time'], # 默认的　objects()
        'collection': 'post_news',
        'shard_key': ('site_id', 'pt_time'),
        'queryset_class': PostQuerySet,
        'indexes':[
            'pt_time',
            '$title',   # text index
            ('data_type', 'site_id'),  # 复合index
        ]
    }

class Trace_Hot_Topic(Document):
	_id = IntField(required=True)
	hot_trace = ListField(IntField(),default=list)
	topic_trace = ListField(StringField(),default=list)
	meta = {
		'ordering' : ['_id'],
		'collection' : 'trace_hot_topic'
	}

class Topic_Relation(Document):
    _id = IntField(required=True,default=0)
    topic_name = StringField(max_length=512)
    topic_relat = ListField(FloatField(),default=0.0)
    meta = {
        'ordering' : ['_id'],
        'collection' : 'topic_relation'
    }

	




class Wall_Post(Document):
    _id = ObjectIdField(primary_key=True)
    url = StringField(required=True, max_length=512,unique=True)
    site_id = IntField(required=True)
    site_name = StringField(max_length=64)
    topic_id = IntField(required=False, default=0)
    hot_topic_id = IntField(required=False, default=0)
    board = StringField(max_length=200)
    data_type = IntField(required=True, choices=DATA_TYPE)
    title = StringField(max_length=500)
    content = StringField(max_length=2048)
    html = FileField()
    pt_time = DateTimeField(required=True)
    # st_time = DateTimeField(default=datetime.datetime.now)
    read_num = IntField(default=0)
    comm_num = IntField(default=0)
    img_url = StringField(max_length=512)
    repost_num = IntField(default=0)
    lan_type = IntField(default=0)
    is_read = IntField(default=0)
    repost_pt_id = StringField(required=False)
    text_type = IntField(required=False)
    phone_num = StringField(max_length=20)
    qq_num = StringField(max_length = 20)
    ip_addr = StringField(max_length=20)
    poster = EmbeddedDocumentField(Poster)

    meta = {
        'ordering': ['-pt_time'], # 默认的　objects()
        'collection': 'wall_post',
        # 'shard_key': ('site_id', 'topic_id', 'pt_time'),
        'queryset_class': PostQuerySet,
        'indexes':[
            'topic_id',
            'pt_time',
            '$title',   # text index
            ('data_type', 'site_id'),  # 复合index
        ]
    }


class Tran_Wall_Post(Document):
    _id = ObjectIdField(primary_key=True)
    url = StringField(required=True, max_length=512,unique=True)
    site_id = IntField(required=True)
    site_name = StringField(max_length=64)
    topic_id = IntField(required=False, default=0)
    hot_topic_id = IntField(required=False, default=0)
    board = StringField(max_length=200)
    data_type = IntField(required=True, choices=DATA_TYPE)
    title = StringField(max_length=500)
    content = StringField(max_length=2048)
    html = FileField()
    pt_time = DateTimeField(required=True)
    # st_time = DateTimeField(default=datetime.datetime.now)
    read_num = IntField(default=0)
    comm_num = IntField(default=0)
    img_url = StringField(max_length=512)
    repost_num = IntField(default=0)
    lan_type = IntField(default=0)
    is_read = IntField(default=0)
    repost_pt_id = StringField(required=False)
    text_type = IntField(required=False)
    phone_num = StringField(max_length=20)
    qq_num = StringField(max_length = 20)
    ip_addr = StringField(max_length=20)
    poster = EmbeddedDocumentField(Poster)
    transText = StringField(max_length=2048)

    meta = {
        'ordering': ['-pt_time'], # 默认的　objects()
        'collection': 'tran_wall_post',
        'shard_key': ('site_id', 'topic_id', 'pt_time'),
        'queryset_class': PostQuerySet,
        'indexes':[
            'topic_id',
            'pt_time',
            '$title',   # text index
            ('data_type', 'site_id'),  # 复合index
        ]
    }



class Sen_Topic(Document):
    _id = IntField(required=True, primary_key=True)
    topic_name = StringField(required=True, max_length=64)
    topic_kws = ListField(StringField(), default=list)
    user_id = IntField(required=True, unique_with='topic_name')
    user_name = StringField(required=True, max_length=32)
    summary = StringField(required=False)   

    meta = {
        'ordering': ['_id'],
        'collection': 'sen_topic'
    }


class Hot_Value_Trace(Document):
    _id = ObjectIdField(primary_key=True)
    date = StringField(max_length=128)
    real_value = IntField(required=True)
    predict_value = IntField(required=True)
    topic_id = IntField(required=True)

    meta = {
        'ordering' : ['_id'],
        'collection' : 'hot_value_trace'
    }


class Topic_evolution(Document):
    _id = ObjectIdField(primary_key=True)
    time = DateTimeField(required=True)
    number = StringField(max_length=128)
    word = StringField(max_length=128)
    topic_id = StringField(max_length=128)

    meta = {
        'ordering' : ['_id'],
        'collection' : 'topic_evolution'
    }

class User(Document):
    _id = ObjectIdField(primary_key=True)
    user_id = IntField(required=True, unique=True)
    user_account = StringField(max_length=128, unique=True)
    user_passwd  = StringField(max_length=128)
    user_logintime = IntField(required=True)
    user_group_id = IntField(required=True, unique_with='user_id')
    user_role_id = IntField(required=True, unique_with='user_id')
    topic_kws = ListField(StringField(), default=list)
    real_name = StringField(required=True, max_length=512)
    phone_num = StringField(required=True, max_length=64)
    email = StringField(required=True, max_length=256)
    img_url = ObjectIdField(required=False)

    meta = {
        'ordering' : ['user_id'],
        'collection' : 'user'
    }

class User_Group(Document):
    _id = ObjectIdField(primary_key=True)
    group_id = IntField(required=True, unique=True)
    group_name = StringField(max_length=128, unique=True)
    meta = {
        'ordering' : ['group_id'],
        'collection' : 'user_group'
    }


class Role_Authority(Document):
    _id = ObjectIdField(primary_key=True)
    role_id = IntField(required=True, unique=True)
    role_name = StringField(max_length=128)
    role_dsp = StringField(max_length=128)
    authority_id = IntField(required=True, unique_with='role_id')
    authority_name = StringField(max_length=128)
    # operate_table = ListField(StringField(), default=list)
    operate_table = DictField()
    operate_type = ListField(StringField(), default=list)
    meta = {
        'ordering' : ['role_id'],
        'collection' : 'role_authority'
    }


class Message(Document):
    _id = ObjectIdField(primary_key=True)
    group_id = IntField(required=True)
    send_user_id = IntField(required=True)
    send_user_acc = StringField(required=True,max_length=128)
    send_user_role = IntField(required=True)
    rec_user_id = IntField(required=True)
    rec_user_acc = StringField(required=True,max_length=128)
    title = StringField(max_length=512)
    content = StringField(max_length=4196)
    is_read = BooleanField(required=True,default=False)
    send_time = DateTimeField(required=True)
    read_time = DateTimeField(required=False)
    desc = StringField(required=False,max_length=1024)
    content_path = ObjectIdField(required=False)


class TiebaPost(Document):
    post_type = IntField(default=1)
    # post basic info
    _id = ObjectIdField(primary_key=True)
    url = StringField(max_length=512)
    thread_id = StringField(max_length=64)
    post_id = StringField(max_length=64, required=True, unique=True)
    floor_num = IntField(default=0)
    comm_num = IntField(default=0)
    pt_time = DateTimeField(required=True)                                   # create datetime
    # st_time = DateTimeField(default=datetime.datetime.now)                   # crawl datetime
    # post detail info
    html = FileField()
    title = StringField(max_length=512)
    content = StringField(max_length=2048)
    video_url = StringField(max_length=512)
    img_url = ListField(StringField(), default=list)
    # author info
    poster = EmbeddedDocumentField(Poster)
    # helper info
    lan_type = IntField(default=0)
    board = StringField(max_length=64)
    site_id = IntField(required=True, default=0)
    site_name = StringField(max_length=64)
    topic_id = ListField(required=False, default=list)
    user_id_list = ListField(IntField(), default=list)
    topic_kwds = ListField(StringField(), default=list)
    data_type = IntField(required=True, choices=DATA_TYPE)
    # adapt database
    hot_topic_id = IntField(required=False, default=0)
    read_num = IntField(default=0)
    repost_num = IntField(default=0)
    is_read = IntField(default=0)
    repost_pt_id = StringField(required=False)
    text_type = IntField(required=False, default=0)
    phone_num = StringField(max_length=20)
    qq_num = StringField(max_length = 20)
    ip_addr = StringField(max_length=20)
    should_pull = BooleanField(required=False,default=False)
    provinces_id_list = ListField(IntField(),default=list)



    meta = {
        'ordering': ['-pt_time'],
        'collection': 'post_tieba',
        # 'shard_key': ('site_id', 'topic_id', 'pt_time'),
        'queryset_class': PostQuerySet,
        'indexes':[
            'topic_id',
            'pt_time',
            '$title',
            ('data_type', 'site_id')
        ]
    }


class Course_Post(Document):
    _id = ObjectIdField(primary_key=True)
    url = StringField(required=True, max_length=512, unique=True)
    site_id = IntField(required=True)
    site_name = StringField(max_length=64)
    topic_id = ListField(IntField(), default=list)
    board = StringField(max_length=200)
    data_type = IntField(required=True)
    title = StringField(max_length=500)
    content = StringField(max_length=2048)
    pt_time = DateTimeField(required=True)
    # st_time = DateTimeField(default=datetime.datetime.now)
    img_url = StringField(max_length=512)
    lan_type = IntField(default=0)
    text_type = IntField(required=False)
    ip_addr = StringField(max_length=20)
    poster = StringField(max_length=64)
    contain_url = ListField(StringField(),default=list)
    point_id = ListField(IntField(),default=list)


    meta = {
        'ordering': ['-pt_time'], # 默认的　objects()
        'collection': 'course_post',
        'shard_key': ('site_id', 'topic_id', 'pt_time'),
        'queryset_class': PostQuerySet,
        'indexes':[
            'topic_id',
            'pt_time',
            '$title',   # text index
            ('data_type', 'site_id'),  # 复合index
        ]
    }





class Sina_follow(Document):
    _id = ObjectIdField(primary_key=True)
    poster_id = StringField(max_length=32, unique=True)
    follows_list = ListField(StringField(), default=list)
    fan_list = ListField(StringField(), default=list)
    home_url = StringField(max_length=512)
    img_url = StringField(max_length=512)
    name = StringField(max_length=64)
    follows = IntField(required=False,unique=False)
    following = IntField(required=False,unique=False)
    post_num = IntField(required=False,unique=False)
    level = StringField(max_length=128)
    location = StringField(max_length=128)
    intro = StringField(max_length=2048)
    birthday = StringField(max_length=128)
    authentication = StringField(max_length=128)
    fan_url = StringField(max_length=512)
    follow_url = StringField(max_length=512)
    abstract = StringField(max_length=128)
    sex = StringField(max_length=64)
    meta = {
        'ordering': ['_id'],
        'collection': 'sina_follow',
        'indexes':['poster_id']
    }

	
class Province_list(Document):
    _id = ObjectIdField(primary_key=True)
    province_name = StringField(max_length=32)
    province_id = IntField(required=True, unique=True)
    province_city_list = ListField(StringField(max_length=64), default=list)
    province_word_cloud = ListField(ListField(),default=list)

    meta = {
        'ordering': ['province_id'],
        'collection': 'province_list'
    }

class ShuiMuType(DocType):

    # url_object_id = Keyword()

    url = Keyword()

    title = Text(analyzer="ik_max_word")

    salary = Keyword()

    job_city = Keyword()

    work_years = Text(analyzer="ik_max_word")

    degree_need = Keyword()

    job_type = Text(analyzer="ik_max_word")

    publish_time = Date()

    tags = Text(analyzer="ik_max_word")

    job_advantage = Text(analyzer="ik_max_word")

    job_desc = Text(analyzer="ik_max_word")

    job_addr = Text(analyzer="ik_max_word")

    company_url = Keyword()

    company_name = Text(analyzer="ik_max_word")

    crawl_time = Date()

    class Meta:
        index = 'shuimu'
        doc_type = "post"
    
    class Index:
        index = 'shuimu'
        doc_type = "post"

   

# min_salary = Integer()

# max_salary = Integer()

   




   

   

if __name__ == "__main__":
    ShuiMuType.init()