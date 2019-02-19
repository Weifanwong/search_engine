import mongoengine
from mongoengine import *
from mongoengine.context_managers import switch_db
import datetime



class ShuiMu_Template(object):
	"""docstring for ShuiMu_Template"""
	def __init__(self, arg):
		super(ShuiMu_Template, self).__init__()
		self.arg = arg
	template_id = IntField(required=True,primary_key=True)
	url = StringField(required=True, max_length=512, unique=True)
	title = StringField(max_length = 128)
	crawl_time =  DateTimeField(default=datetime.datetime.now)
	pt_time = StringField(max_length =128)
	gender = StringField(max_length = 4)
	content = StringField(max_length=2048)

		