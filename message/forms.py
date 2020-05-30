from django import forms
from .models import SendMessage, SupportModel



class SendMessageForm(forms.ModelForm):
    """a form for sending message that includes all fields except sender, reciever and is_readed

    Arguments:
        forms {MODULE} -- a django built-in Model Form
    """    
    class Meta:
        model = SendMessage
        exclude = ['sender', 'receiver', 'is_readed']

        
class SupportForm(forms.ModelForm):
    """a model form to send errors from registeration process

    Arguments:
        forms {MODULE} -- a django built-in Model Form
    """    
    class Meta:
        model = SupportModel
        fields = ['content', 'name']