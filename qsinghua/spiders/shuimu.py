# -*- coding: UTF-8 -*-
import scrapy
from urllib import *
import json
# from urllib.parse import urlencode
import requests 
from mongoengine import *
from qsinghua.items import ShuiMuPostItem
import sys
import importlib
# from PIL import Image
# importlib.reload(sys)
import importlib,sys 
# importlib.reload(sys)
# sys.setdefaultencoding("utf-8")


conn = connect('wwf_database02', alias='default', host='127.0.0.1', port=27017, username='', password='')


class ShuimuSpider(scrapy.Spider):
	name = 'shuimu'
	# allowed_domains = ['www.com']
	# start_urls = ['http://www.newsmth.net/nForum/user/ajax_login.json']
	headers = {
	'Accept': 'application/json, text/javascript, */*; q=0.01',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language':'en,en-US;q=0.9,zh-CN;q=0.8,zh;q=0.7',
	# 'Content-Length': '45'
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'Cookie': 'NFORUM=rmg4r41gj6rraaulq8ipc75oq5; main[XWJOKE]=hoho; main[UTMPUSERID]=guest; main[UTMPNUM]=47430; Hm_lvt_bbac0322e6ee13093f98d5c4b5a10912=1544933168,1544933353,1544954402; Hm_lpvt_bbac0322e6ee13093f98d5c4b5a10912=1544954402; main[UTMPKEY]=37814499',
	'Host': 'www.newsmth.net',
	'Origin': 'http://www.newsmth.net',
	'Proxy-Connection': 'keep-alive',
	'Referer': 'http://www.newsmth.net/',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
	'X-Requested-With': 'XMLHttpRequest',
    } 
	formdata = {
    'id': 'q836754578',
    'passwd': 'wangqiang654321',
    'mode': '0',
    'CookieDate':'0',
    }
	url = 'http://www.newsmth.net/nForum/user/ajax_login.json'
	headers1 = {
	'Host':'www.newsmth.net',
	'Upgrade-Insecure-Requests':'1',
	'DNT':'1',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Referer':	'http://www.newsmth.net/',
	'Accept-Encoding':	'gzip, deflate',
	'Accept-Language':	'zh-CN,zh;q=0.9,en;q=0.8',
	'Cookie':	'Hm_lvt_bbac0322e6ee13093f98d5c4b5a10912=1544963456; Hm_lpvt_bbac0322e6ee13093f98d5c4b5a10912=1544964807; main[UTMPUSERID]=q836754578; main[UTMPKEY]=49445247; main[UTMPNUM]=9696',
	'If-Modified-Since':'Sun, 16 Dec 2018 12:36:33 GMT'
	}
	headers2 = {
	'Accept': '*/*',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language':'en,en-US;q=0.9,zh-CN;q=0.8,zh;q=0.7',
	'Cookie':' NFORUM=rmg4r41gj6rraaulq8ipc75oq5; main[XWJOKE]=hoho; Hm_lvt_bbac0322e6ee13093f98d5c4b5a10912=1544933168,1544933353,1544954402; main[UTMPUSERID]=q836754578; main[UTMPKEY]=24609885; main[UTMPNUM]=12725; Hm_lpvt_bbac0322e6ee13093f98d5c4b5a10912=1545013513',
	'Host': 'www.newsmth.net',
	'If-Modified-Since': 'Mon, 17 Dec 2018 02:24:03 GMT',
	'Proxy-Connection': 'keep-alive',
	'Referer': 'http://www.newsmth.net/nForum/',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
	'X-Requested-With': 'XMLHttpRequest',
	}

	def start_requests(self):
		yield scrapy.FormRequest(self.url ,formdata = self.formdata,headers = self.headers, callback = self.parse)

	def parse(self, response):
		url_2 = 'http://www.newsmth.net/nForum/section/1?ajax'
		yield scrapy.Request(url = url_2, headers = self.headers2, callback = self.after_login)
        
	def after_login(self,response):
		# item = ShuiMuPostItem()
		school_url = response.xpath('//td[@class="title_1"]/a/@href').extract()
		# print(len(school_url1))
		base_url = 'http://www.newsmth.net'
		param = {'p':1}
		for school in school_url:
			for page in range(1,2):
				param['p'] = page
				url = base_url + school + '?ajax&' +urlencode(param)
				yield scrapy.Request(url = url, headers = self.headers2, callback = self.school_page)

	def school_page(self,response):
		item = ShuiMuPostItem()
		topic_info = []
		topic_url = response.xpath('//td[@class="title_9"]/a/@href').extract()
		topic_date = response.xpath('//td[@class="title_10"]/text()').extract()
		base_url = 'http://www.newsmth.net'

		for ele in range(len(topic_url)):
			topic_info.append([topic_url[ele],topic_date[ele]])
		# print(topic_info)

		for topic in topic_info:
			url = base_url + topic[0]
			item['url'] = url
			item['pt_time'] = topic[1]
			yield scrapy.Request(url = url, headers = self.headers2, meta = {'item':item},callback = self.post)
		# print(response.text)
		# print(response.url)

	def post(self,response):
		item = response.meta['item']
		poster = response.xpath('//span[@class="a-u-name"]/a/text()').extract()[0]  #提取发帖人名称
		title = response.xpath('//body//span[@class="n-left"]/text()').extract()[0]
		title = title.replace('文章主题:','') #帖子名称
		comm_num = response.xpath('//body//li[@class="page-pre"]/i/text()').extract()[0]
		content = response.xpath('//body//td[@class="a-content"]/p').extract()[0]
		# content = content.replace('\xa0','')
		# content = content.replace('<br>','')
		poster_num = response.xpath('//body//tr[@class="a-body"]/td[@class="a-left"]//dl[@class="a-u-info"]//dd/text()').extract()[1]
		# print(response.url)
		item['poster_name'] = poster
		item['title'] = title
		item['comm_num'] = int(comm_num)
		item['content'] = content
		item['url'] = response.url
		item['site_name'] = '水木论坛'
		item['poster_num'] = int(poster_num)
		item["site_id"] = 1

		base_url = 'http://www.newsmth.net/nForum/user/query/'
		poster_url = base_url + item['poster_name'] + '.json'
		# print(poster_url)
		yield scrapy.Request(url = poster_url,headers = self.headers2, meta={'item':item},callback = self.poster)
		# print(item)
		# print(poster)
		# yield item

	def poster(self,response):
		item = response.meta['item']
		poster_info = response.text
		poster_info = poster_info.replace('false','0')
		poster_info = poster_info.replace('true','1')
		poster_info = eval(poster_info)
		if poster_info['gender'] == 'm':
			item['poster_sex'] = '男'
		elif poster_info['gender'] == 'f':
			item['poster_sex'] = '女'
		else:
			item['poster_sex'] = ''
		# print(item)
		yield item
