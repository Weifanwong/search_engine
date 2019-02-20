"""yqapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
# from yqdata import views, views_topics, views_realtime_monitor, views_dashboard, views_settings, views_senmassage, views_hot_topic, views_search, views_retrieval, views_sen_topic,views_users,views_translate, views_usermessage, views_login, es_test, views_pull, views_pull_socket, views_knownledge
import views_template
# from websocketdata import views_socket

urlpatterns = [
    url(r'^train_search_get$',views_template.Homework_Get_Show.as_view()),
    url(r'^train_search_post$',views_template.Homework_Post_Show.as_view()),
    #url(r'^yqdata/train_delete_get$',views_template.Template_Delete_1.as_view()),
]
