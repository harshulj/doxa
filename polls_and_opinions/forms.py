from django import forms
from models import *

class PollModelChoiceField(forms.ModelChoiceField):
    '''
        Special model choice for the Choice field in the PollVoteForm.
        This is to enable us to create dynamic labels on the fly for the
        choice field.
    '''
    def label_from_instance(self, obj):
        return "%s  (%s)"%(obj.__unicode__(),len(obj.votes.all()))
        

class PollVoteForm(forms.Form):
    '''
        Form for rendering a poll for voting.
        The keyword argument 'poll' must be specified for sure.
        The form is dynamically created based on the poll specified.
    '''
    # This field must be initialized with the appropriate poll id whenever it is created.    
    def __init__(self, poll,*args, **kwargs):  
        super(PollVoteForm,self).__init__(*args,**kwargs)      
        
        # introduce both the poll as a hidden field.
        self.fields['poll_id'] = forms.CharField(widget=forms.HiddenInput)
        self.fields['poll_id'].initial = poll.id
        
        # Choices are presented as a choice field in radio select
        self.fields['choice'] = PollModelChoiceField(label="Choices",queryset=poll.choices.prefetch_related('votes').all(), widget=forms.RadioSelect)
        # If an initial value was specified for the choices
        if kwargs.has_key('initial') and kwargs['initial'].has_key('choice'):
            self.fields['choice'].initial = kwargs['initial']['choice']
        # Get rid of the empty choice ( ------ )
        self.fields['choice'].empty_label = None

def get_poll_vote_form(poll,choice=None):
    '''
        Helper method that creates and appropriate PollVoteForm
        If a valid choice is specified, the choice is put in as the initial
        value
    '''
    if ( not choice is None ) and choice.poll == poll:
        return PollVoteForm(poll,initial={'choice' : choice})
    else:
        return PollVoteForm(poll)
    
    
class OpinionForm(forms.Form):
    '''
    Form for creating an opinion.
    '''
    # The hidden fields to identify the object to which this Opinion is related.
    # The min_value on these fields is set to 0 coz they are primary keys.
    object_id = forms.IntegerField(widget=forms.HiddenInput, required=False, min_value=0)
    content_type_id = forms.IntegerField(widget=forms.HiddenInput, required=False, min_value=0)
    text = forms.CharField(widget = forms.Textarea, required=False)
    
    def __init__(self, *args, **kwargs):
        '''
        Overriden init to make sure that either both the object_id and content_type_id are provided
        when initializing the form or both of them are not provided.
        '''
        if kwargs.has_key('initial'):
            object_id = kwargs['initial'].get('object_id',0)
            content_type_id = kwargs['initial'].get('content_type_id',0)
            if bool(object_id) ^ bool(content_type_id):
               #if one of them is not set while the other is,
               raise AttributeError("object_id and content_id must both be set or not set.")
        super(OpinionForm,self).__init__(*args,**kwargs)

