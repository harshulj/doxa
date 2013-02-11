from django.utils.timezone import now
from haystack.indexes import *
from haystack import site
from haystack import indexes
from polls_and_opinions.models import Opinion, Poll

class OpinionIndex(SearchIndex):
	"""
		Search Index for Opinion model.
	"""
	text = CharField(document=True, use_template=True)
	author = CharField(model_attr='author')
	created_on = DateTimeField(model_attr='created_on')

	def index_queryset(self):
		return Opinion.objects.filter(created_on__lte=now())

class PollIndex(SearchIndex):
	"""
		Search Index for Poll model.
	"""
	text = CharField(document=True, use_template=True)
	author = CharField(model_attr='author')
	is_live = BooleanField(model_attr='is_live')
	question_auto = indexes.EdgeNgramField(model_attr='question')

	def index_queryset(self):
		return Poll.objects.filter(created_on__lte=now())

site.register(Poll, PollIndex)
site.register(Opinion, OpinionIndex)
