'''
    Models for polls_and_opinions app
'''

__author__ = 'Raj Kamal Singh'
__email__ = 'rkssisodiya@gmail.com'
__status__ = 'development'

from django.conf.urls.defaults import *
from models import *
from views import *
from django.views.generic.list_detail import object_detail, object_list

APP_NAME = 'polls_and_opinions'

poll_info = {'queryset': Poll.objects.all(),
             'paginate_by' : 20,
             }

urlpatterns = patterns('',
                       url(r'^$',poll_list,name=APP_NAME+"_polls_list"),
                       url(r'^(?P<poll_id>\d+)$',poll_detail,name=APP_NAME+"_poll_detail"),
                       )