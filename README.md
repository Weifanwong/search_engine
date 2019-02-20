# qsinghua
我的搜索引擎主要分为三部分
#1 数据爬取：利用scrapy框架选择几个新闻网站作为爬取对象，爬取到的数据保存在本地的mongodb中。每一条数据主要包含title、url、content。

#2 elasticsearch：利用elasticsearc可以从mongodb中读取数据，同时完成倒排索引、排序，从而返回具有一定合理性的结果（list）。

#3 django： 后端是用django写的，主要用来实现查找api。

#4 html/js/css： 用来搭建前端。

整体的思路： 通过前端网页输入查询内容，将查询字段利用ajax的get请求发送给django服务器，调用查询api，在查询api中调用es，使查询的结果一定的顺序返回。
返回的数据再次显示到前端网页中。

使用方法：
1、scrapy运行qsinghua爬虫（这是一个demo，只能爬取水木论坛的部分数据），囤积数据。
../qsinghua
scrapy crawl shuimu

2、运行服务器 
../search_engin/search_engin
python manage.py runserver 8000

3、打开search_engine.html，输入查询内容，点击搜索