'''
    Models for polls_and_opinions app
'''

__author__ = 'Raj Kamal Singh'
__email__ = 'rkssisodiya@gmail.com'
__status__ = 'development'

from django.conf.urls.defaults import *
from polls_and_opinions.models import *
from polls_and_opinions.views import *

APP_NAME = 'polls_and_opinions'

poll_info = {'queryset': Poll.objects.all(),
             'paginate_by' : 20,
             }

urlpatterns = patterns('',
                       url(r'^$',poll_list,name=APP_NAME+"_polls_list"),
                       url(r'^(?P<id>\d+)$',poll_detail,name=APP_NAME+"_poll_detail"),
                       )