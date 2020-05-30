from django import forms
from django.contrib.auth import authenticate
from startup.models import StartUp, Referee, Requests, ShetabDahande, TeamMember
from usercp.models import User



class StartUpForm1(forms.ModelForm):   
    """this model form is for the 3rd stage of registering process that will get title, prototype, invesment, province, city

    Arguments:
        forms {MODULE} -- a django built-in Model Form
    """                          
    class Meta:
        model = StartUp
        fields = ('title', 'prototype', 'investment', 'province_startup', 'city_startup', 'explain_startup',)


class StartUpForm2(forms.ModelForm):
    """this StartUp model form is for the stage that startups owner will upload a video that discribe the startup

    Arguments:
        forms {MODULE} -- a django built-in Model Form
    """    
    class Meta:
        model = StartUp
        fields = ('video',)




class StartUpForm5(forms.ModelForm):
    """this StartUp model form is for the team stage that will get information about team

    Arguments:
        forms {MODULE} -- a django built-in Model Form
    """    
    class Meta:
        model = StartUp
        fields = ('how_mem_meet', 'what_m_better', 'what_u_need', 'who_sent_you',)

class StartUpForm3(forms.ModelForm):
    """this StartUp model form is for PDeck stage that will get information about Startup

    Arguments:
        forms {MODULE} -- a django built-in Model Form
    """    
    class Meta:
        model = StartUp
        fields = ('problem',
                  'about_start',
                  'mysolution',
                  'solution',
                  'market_size',
                  'defect',
                                )


class StartUpForm4(forms.ModelForm):
    """this StartUp model form is for geting the PDeck file

    Arguments:
        forms {MODULE} -- a django built-in Model Form
    """    
    class Meta:
        model = StartUp
        fields = ('attachfile_p',)

class StartUpForm6(forms.ModelForm):
    """this StartUp model form is for getting financial information

    Arguments:
        forms {MODULE} -- a django built-in Model Form
    """    
    class Meta:
        model = StartUp
        fields = ('attachfile_e',)


class TeamMembersForm(forms.ModelForm):
    """this is TeamMember model form that will get all the information about team but excludes the user and startup field

    Arguments:
        forms {MODULE} -- a django built-in Model Form
    """    
    class Meta:
        models = TeamMember
        exclude = ('user', 'startup')


class ShetabDahandeForm(forms.ModelForm):
    """this is ShetabDahande(accelerator) model form that includes all fields except user and category

    Arguments:
        forms {MODULE} -- a django built-in Model Form
    """    
    class Meta:
        model = ShetabDahande
        exclude = ('user', 'category')


class RefereeForm(forms.ModelForm):
    """this is the Referee model form that only gets the comment of referee in the information page

    Arguments:
        forms {MODULE} -- a django built-in Model Form
    """    
    class Meta:
        model = Referee
        fields = ('score_comment',)


class RequestsForm(forms.ModelForm):
    """this is Requests model form that get request information for money

    Arguments:
        forms {MODULE} -- a django built-in Model Form
    """    
    class Meta:
        model = Requests
        fields = ('request_title', 'request_money',
                  'request_cat', 'request_expression',)




