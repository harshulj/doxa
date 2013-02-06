'''
    Contains all the admin directives for polls_and_opinions
'''

__author__ = 'Raj Kamal Singh'
__email__ = 'rkssisodiya@gmail.com'
__status__ = 'development'

from models import *
from django.contrib import admin
from django.contrib.admin.templatetags.admin_list import date_hierarchy

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 1

class PollAdmin(admin.ModelAdmin):
    date_hierarchy = 'published_on'
    search_fields = ['question','author']
    list_filter = ['author', 'is_live']
    list_display = ['__unicode__','author','is_live','published_on','duration','last_modified_on']
    
    inlines = [ChoiceInline,]

class VoteAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    search_fields = ['voter','choice']
    list_filter = ['voter', 'choice']
    list_display = ['__unicode__','created_on']
    
class OpinionAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    search_fields = ['author','text']
    list_filter = ['author']
    list_display = ['__unicode__','author','content_type','content_object','created_on']
    
admin.site.register(Poll, PollAdmin)
admin.site.register(Vote,VoteAdmin)
admin.site.register(Opinion, OpinionAdmin)