from django import forms
from models import *

class PollVoteForm(forms.Form):
    '''
        Form for rendering a poll for voting.
        The keyword argument 'poll' must be specified for sure.
        The form is dynamically created based on the poll specified.
    '''
    # This field must be initialized with the appropriate poll id whenever it is created.    
    def __init__(self, poll, *args, **kwargs):
        super(PollVoteForm,self).__init__(*args,**kwargs)
        
        # introduce both the poll and the Choices
        self.fields['poll_id'] = forms.CharField(widget=forms.HiddenInput)
        self.fields['poll_id'].initial = poll.id
        
        self.fields['choice'] = forms.ModelChoiceField(queryset=poll.choices.all(), widget=forms.RadioSelect)
        if kwargs.has_key('initial') and kwargs['initial'].has_key('choice'):
            self.fields['choice'].initial = kwargs['initial']['choice']
