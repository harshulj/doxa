import datetime
from haystack.indexes import *
from haystack import site
from polls_and_opinions.models import Opinion, Poll

class OpinionIndex(SearchIndex):
	text = CharField(document=True, use_template=True)
	author = CharField(model_attr='author')
	created_on = DateTimeField(model_attr='created_on')
	
	def index_queryset(self):
		return Opinion.objects.filter(created_on__lte=datetime.datetime.now())

site.register(Opinion, OpinionIndex)
