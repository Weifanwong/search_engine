from datetime import datetime
from elasticsearch_dsl import DocType, Date, Nested, Boolean,analyzer, Completion, Keyword, Text, Integer

from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.analysis import CustomAnalyzer

connections.create_connection(hosts=['127.0.0.1'])

class Analyzer(CustomAnalyzer):
    def get_analysis_definition(self):
        return {}

ik_analyzer = Analyzer('ik_max_word', filter=['lowercase'])


class ShuimuType(DocType):  # 
    title = Text(analyzer="ik_max_word")
    content = Text(analyzer="ik_max_word")
    article_id = Keyword()
    origin_url = Keyword()
    author = Keyword()
    pub_time = Date()


    class Index:
        name = 'my-index'
        # doc_type = 'jianshu'
        # index = "scrapy"


if __name__ == "__main__":
    ShuimuType.init()