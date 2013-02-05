from django.conf.urls.defaults import *
from models import *
from django.views.generic.list_detail import object_detail, object_list

poll_info = {'queryset': Poll.objects.all(),
             'paginate_by' : 20,
             }

urlpatterns = patterns('',
                       url(r'^$',object_list,poll_info,name="doxa_polls_poll_list"),
                       url(r'^(?P<object_id>\d+)$',object_detail,poll_info,name="doxa_polls_poll_detail"),
                       )