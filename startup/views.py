from django.utils.decorators import method_decorator
from dateutil.relativedelta import relativedelta
from io import BytesIO
from django.core import files
import tempfile
import requests
from urllib.request import urlopen
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth import authenticate, login, logout
from dateutil import parser
from django.views.generic import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from random import randint
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from django.forms.models import model_to_dict

from django.contrib.sites.shortcuts import get_current_site
from urllib.parse import urlsplit
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from . import models
from usercp.models import Role, User
from category.models import Categories
from theevent.models import LeaderModel
from message.models import SendMessage, SupportModel
from usertracker.models import UserTracker
from django.core.paginator import Paginator
import uuid
import pickle
from django_user_agents.utils import get_user_agent
from django.contrib.auth import update_session_auth_hash
from startups.engine import sms
from startup.forms import (StartUpForm1,
                           TeamMembersForm,
                           StartUpForm2,
                           StartUpForm3,
                           StartUpForm5,
                           ShetabDahandeForm,
                           RefereeForm,
                           RequestsForm,
                           StartUpForm4,
                           StartUpForm6,

                           )

from category.forms import CategoryForm
from message.forms import SupportForm, SendMessageForm
from usercp.forms import (UserRegisterForm,
                          UserCreateRole,
                          LeaderForm,
                          LeaderUserForm,
                          KarmandForm,
                          ProfileAdminForm,
                          ProfileRoleForm,
                          PasswordChangeForm,
                          )
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.files.base import ContentFile

from django.db.models import Q
import json
from threading import Thread
from django.core import serializers
import base64
import re

from persiantools.jdatetime import JalaliDate, JalaliDateTime
from datetime import datetime
from django.utils import timezone

from django.utils.timezone import make_aware
from startups.utils import get_client_ip, premession, logging_view, status_of_user, send_email, get_list, get_list2, resize_pics, create_notification
from django.contrib.admin.models import LogEntry

import logging
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.views import LoginView
from .services import *
logger = logging.getLogger(__name__)

# Create your views here.





@logging_view
@login_required(login_url='usercp:login')
# @user_tracker()
@premession(th_type1='manager', th_type2='karmand', role=['operational', ])
def list_startup(request):
    """show the list of all startups with searchable features

    Arguments:
        request {REQUEST} -- to define method for search and paginations

    Returns:
        RENDER -- renders queryset of StartUp model
    """
    search = {
        'name': request.GET.get('startup_search'),
        'status': request.GET.get('status'),
        'the_phone': request.GET.get('phone'),
        'lname': request.GET.get('lname_search'),
        'shetab': request.GET.get('shetab_search'),
        'email': request.GET.get('email_search'),
        'cat_id': request.GET.get('cats'),
        'province': request.GET.get('province'),
        'city': request.GET.get('city'),
        'start_date': request.GET.get('start_date'),
        'end_date': request.GET.get('end_date'),
    }
    offset = request.GET.get('page')

    return render(request, 'startup/list-startup.html', list_startup_service(request.track_info, offset, search))


@logging_view
@login_required(login_url='usercp:login')
# @user_tracker()
def select_startup(request):
    """allow operationals to selecte an startup as chosen startup and then the selected startup can see the coaches schedule

    Arguments:
        request {REQUSET} -- to define method and check if it's an ajax request and track user

    Returns:
        JSONRESPONSE -- returns json response for ajax
    """    
    if request.is_ajax():
        startup_id = request.POST.get('add_id')
        return JsonResponse(select_startup_service(startup_id, request.track_info))
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))





@logging_view
@login_required(login_url='usercp:login')
# @user_tracker()
def delete_startup(request):
    """allow operationals to delete an startup

    Arguments:
        request {REQUEST} -- to define method and track user and check if it's an ajax request

    Returns:
        JSONRESPONSE -- returns json response for ajax
    """    
    if request.is_ajax():
        startup_id = request.POST.get('delete_id')
        return JsonResponse(delete_startup_service(startup_id, request.track_info))
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@logging_view
@premession(th_type1='manager',  role=['operational', ])
# @user_tracker()
def list_referee(request):
    """list of referees

    Arguments:
        request {REQUEST} -- to define page number track user and search

    Returns:
        RENDER -- renders querysets of referess
    """ 
    search = {
    'fname': request.GET.get('fname_search'),
    'lname': request.GET.get('lname_search'),
    'mobile': request.GET.get('mobile_search'),
    }
    offset = request.GET.get('page')
    return render(request, 'startup/list-referee.html', list_referee_service(request.track_info, search, offset))


@logging_view
@login_required(login_url='usercp:login')
@premession(th_type1='manager',  role=['operational', ])
# @user_tracker()
def list_investor(request):
    """list of all users that have the role of investor

    Arguments:
        request {REQUEST} -- GET method for search and POST method for investor_can see startup

    Returns:
        RENDER -- renders the list-investor html file
    """    
    context = {}
    search = {
            "fname": request.GET.get('fname_search'),
            "lname": request.GET.get('lname_search'),
            "mobile": request.GET.get('mobile_search'),
            }
    offset = request.GET.get('page')
    investors = list_investor_service(request.track_info, search, context, offset)
    if request.method == 'POST':
        can_see = request.POST.get('submit_looks')
        list_investor_activate_service(investors, request.track_info, can_see)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    return render(request, 'startup/list-investor.html', context)


@logging_view
@login_required(login_url='usercp:login')
# @user_tracker()
def investor_can_see(request):
    """make user to see startups that have the status of add_to_invest

    Arguments:
        request {REQUEST} -- to define if it's ajax request

    Returns:
        JSONRESPONSE -- returns data for ajax
    """    
    if request.is_ajax():
        inv_id = request.POST.get('add_id')
        return JsonResponse(investor_can_see_service(inv_id, request.track_info))
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@logging_view
@login_required(login_url='usercp:login')
@premession(th_type1='manager',  role=['operational', ])
# @user_tracker()
def list_coach(request):
    """list of all users with role of leader and coach

    Arguments:
        request {REQUEST} -- to get entered values for search and offset

    Returns:
        RENDER -- renders the list of all coaches and leaders
    """    
    search = {
    'fname': request.GET.get('fname_search'),
    'lname': request.GET.get('lname_search'),
    'mobile': request.GET.get('mobile_search'),
    }
    offset = request.GET.get('page')
    
    return render(request, 'startup/list-coach.html', list_coach_service(request.track_info, offset, search))


@logging_view
@login_required(login_url='usercp:login')
@premession(th_type1='manager',  role=['operational', ])
# @user_tracker()
def list_accelerator(request):
    """show the list of all accelerators 

    Arguments:
        request {REQUEST} -- to get pagination and track user

    Returns:
        RENDER -- renders list of accelerators on list-accelerator html file
    """    
    offset = request.GET.get('page')
    return render(request, 'startup/list-accelerator.html', list_accelerator_serviece(request.track_info, offset))


@logging_view
@login_required(login_url='usercp:login')
# @user_tracker()
def delete_accelerator(request):
    """an ajax request to delete seleced accelerator

    Arguments:
        request {REQUEST} -- to define method and check the if request is ajax

    Returns:
        JSONRESPONSE -- returns data for ajax
    """    
    if request.is_ajax():
        acc_id = request.POST.get('delete_id')
        return JsonResponse(delete_accelerator_service(request.track_info, acc_id))
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@logging_view
@login_required(login_url='usercp:login')
# @user_tracker(model='startup')
def suspend_startup(request, startup_id):
    """allow operational to suspend the startup

    Arguments:
        request {REQUEST} -- to get values and check the method
        id {INT} -- the id of the selected startup

    Returns:
        HTTPRESPONSEREDIRECT -- redirect the user to the current page after submiting form
    """    
    startup = get_startup_service(id=startup_id)
    if request.method == "POST":
        form = request.POST
        suspend_startup_service(form, startup, request.track_info)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@logging_view
# @user_tracker(model='startup')
def verify_startup_documents(request, startup_id):
    """accept or decline startups documents by operationals

    Arguments:
        request {REQUEST} -- to define method and get some values from operational
        id {INT} -- the id of selected startup

    Returns:
        HTTPRESPONSEREDIRECT -- redirect the user to the current page after submiting form
    """    
    startup = get_startup_service(id=startup_id)
    if request.method == "POST":
        form = request.POST
        verify_startup_documents_service(form, startup, request.track_info)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@logging_view
# @user_tracker(model='startup')
def startup_assessment(request, startup_id):
    """get the startup by id and set new status for assessment of startup

    Arguments:
        request {REQUEST} -- to define method and get entered values
        id {INT} -- the id of the startup

    Returns:
        HTTPRESPONSEREDIRECT -- redirect the user to the current page after submiting form
    """    
    startup = get_startup_service(id=startup_id)
    if request.method == "POST":
        form = request.POST
        startup_status_service(form, request.track_info, startup)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@logging_view
# @user_tracker(model='startup')
def verify_not_presence_referee(request, startup_id):
    """operational will set new status for startup if it's the not presence referee accepted or failed

    Arguments:
        request {REQUEST} -- to define method and save entered comments and values
        id {INT} -- the id of selected startup

    Returns:
        HTTPRESPONSEREDIRECT -- redirect the user to the current page after submiting form
    """    
    startup = get_startup_service(id=startup_id)
    if request.method == "POST":
        form = request.POST
        verify_not_presence_referee_service(form, startup, request.track_info)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@logging_view
# @user_tracker(model='startup')
def verify_presence_referee(request, startup_id):
    """operational will set new status for startup if it's the presence referee accepted or failed

    Arguments:
        request {REQUEST} -- to define method and save entered comments and values
        id {INT} -- the id of selected startup

    Returns:
        HTTPRESPONSEREDIRECT -- redirect the user to the current page after submiting form
    """   
    startup = get_startup_service(id=startup_id)
    if request.method == "POST":
        form = request.POST
        verify_presence_referee_service(form, startup, request.track_info)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))



@logging_view
# @user_tracker(model='startup')
def add_to_investor(request, startup_id):
    """operational will set new status for startup after the presence referee accepted
       to add_investor in this status startup can be seen by investors for investment

    Arguments:
        request {REQUEST} -- to define method and save entered comments and values
        id {INT} -- the id of selected startup

    Returns:
        HTTPRESPONSEREDIRECT -- redirect the user to the current page after submiting form
    """   
    startup = get_startup_service(id=startup_id)
    if request.method == "POST":
        form = request.POST
        add_to_investor_service(form, startup, request.track_info)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@logging_view
@login_required(login_url='usercp:login')
# @user_tracker()
def add_for_invest(request):
    """allow investor to accpet or decline meeting with startups which have status of add_investor

    Arguments:
        request {REQUEST} -- to check if request is ajax and track user

    Returns:
        HTTPRESPONSEREDIRECT -- redirect the user to the current page after submiting form
    """    
    if request.is_ajax():
        startup_id = request.POST.get('startup_id')
        return JsonResponse(add_for_invest_service(startup_id, request.user, request.track_info))
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@logging_view
@login_required(login_url='usercp:login')
# @user_tracker()
def reconsider(request):
    """this view only will be shown in stage of verifying startup status if it's decliented (failed)
       to give startup another chance to edit some information

    Arguments:
        request {REQUEST} -- to define if it's ajax request

    Returns:
        JSONRESPONSE -- returns data for ajax
    """    
    if request.is_ajax():
        startup_id = request.POST.get('acceptid')
        comment = request.POST.get('admin_comment_apply')
        return JsonResponse(reconsider_service(startup_id, comment, request.track_info))
    return HttpResponseRedirect(request.META.get("HTTP_REFEREE"))


@logging_view
@login_required(login_url='usercp:login')
@premession(th_type1='manager', th_type2='startup', role=['operational', ])
def edit_startup(request, startup_id):
    """operational or manage or admin can edit specified startup, owner, team members informations

    Arguments:
        request {REQUEST} -- to check the method and get entered values and track user
        id {INT} -- the id of startup

    Returns:
        RENDER -- renders the startup/owner/team members instances 
    """    
    context = {}
    if edit_startup_instance_service(startup_id, request.user, request.track_info, context) == "not_allowed":
        return redirect('usercp:dashboard_panel')
    userprofile, startup, team_member = edit_startup_instance_service(startup_id, request.user, request.track_info, context)
    if request.method == "POST":
        form = request.POST
        file_value = request.FILES
        forms = edit_startup_service(startup, request.user, userprofile, form, file_value, request.track_info, team_member)
        if forms == True:
            return HttpResponseRedirect(startup.get_absolute_url())
        else:
            logger.error(f'startupform1: {forms[0].errors}--startupform4: {forms[1].errors}-- startupform5:{forms[2].errors}-- startupform6: {forms[3].errors}-- startupform3: {forms[4].errors}-- userprofile_form: {forms[5].errors}-- leader_form: {forms[6].errors}')
            messages.warning(request, f'startupform1: {forms[0].errors}--startupform4: {forms[1].errors}-- startupform5:{forms[2].errors}-- startupform6: {forms[3].errors}-- startupform3: {forms[4].errors}-- userprofile_form: {forms[5].errors}-- leader_form: {forms[6].errors}', extra_tags='edit_startup_form_error')

    return render(request, 'startup/edit-startup.html', context)


@logging_view
@login_required(login_url='usercp:login')
@premession(th_type1='manager',  role=['operational', ])
# @user_tracker(model='shetabdahande')
def edit_accelerator(request, shetabdahande_id):
    """allow admin, manager, operational to edit specific accelerator

    Arguments:
        request {REQUEST} -- to define method and get entered values
        id {INT} -- the id of accelerator object

    Returns:
        RENDER -- renders the edit-accelerator html file with instances of accelerator
    """    
    context = {}
    shetab = edit_accelerator_instance_service(shetabdahande_id, context)
    if request.method == "POST":
        form = request.POST
        accelerator_form = edit_accelerator_service(form, shetab, request.track_info)
        if accelerator_form == True:
            return redirect('startup:list_accelerator')
        else:
            messages.warning(request, str(accelerator_form),
                             extra_tags='edit_shetab_form_error')
    return render(request, 'startup/edit-accelerator.html', context)


@logging_view
@login_required(login_url='usercp:login')
# @user_tracker(model='startup')
def information_startup(request, startup_id):
    """informaion about selected startup such as:
       - problem
       - mysolution
       - solution
       - market_size
       - defect
       - attachfile_p
       - attachfile_e

    Arguments:
        request {REQUEST} -- to pass to template as context
        id {INT} -- the id of selected startup

    Returns:
        RENDER -- renders the startups informaion
    """
    startup = get_startup_service(id=startup_id)
    return render(request, 'startup/information-startup.html', {'startup': startup})


@logging_view
@login_required(login_url='usercp:login')
@premession(th_type1='manager',  role=['operational', ])
# @user_tracker(model='shetabdahande')
def information_accelerator(request, shetabdahande_id):
    """a detailed informaion about an accelerator

    Arguments:
        id {INT} -- the id of seleclted accelerator object

    Returns:
        RENDER -- renders information about selected accelerator
    """    
    return render(request, 'startup/information-accelerator.html', informaion_accelerator_service(shetabdahande_id, request.track_info))


@logging_view
@login_required(login_url='usercp:login')
@premession(th_type1='manager',  role=['operational', ])
# @user_tracker(model='shetabdahande')
def create_accelerator(request):
    """allow operational or admin or manager to create new accelerator(shetab dahande)

    Arguments:
        request {REQUEST} -- to define method and get entered values and track_user

    Returns:
        RENDERS -- rendres caregories and ShetabDahandeForm to create-accelerator html file
    """    
    if request.method == "POST":
        form = request.POST
        shetab_form = create_accelerator_service(form, request.track_info)
        if shetab_form == True:
            return redirect('startup:list_accelerator')
        else:
            messages.warning(request, str(shetab_form),
                             extra_tags='shetab_form_error')

    return render(request, 'startup/create-accelerator.html', create_accelerator_instances())


@logging_view
@login_required(login_url='usercp:login')
# # @user_tracker(model='startup')
@premession(th_type1='manager',  role=['operational', 'referee', ])
def information(request, startup_id):
    """this is the informaion page for startup
       this page has some dependent steps which operational decide 
       startup should pass the step or not
       steps:
       1 - verification of document startup
       2 - verification of status of startup
       3 - select leader (rahbar_asli) for startup
       4 - select not presence referees for startup
       5 - select presence referess for startup
       6 - not presence referees should give scores to startup
       7 - presence referees should give scores to startup
       8 - operational should accept or decline startups not presence referee status
       9 - operational should accept or decline startups presence referee status
       10 - startup status can change to add_investor for investment
       * there is suspend status that can be apply to startup on any step
       * operational will be choosen as presence referee and not presence referee automatically
         cause he can score the startup instead of referees

    Arguments:
        request {REQUEST} -- to defince requested user/track user/method
        id {INT} -- the id of selected startup

    Returns:
        RENDRER -- renders startups informations/scores if available/owner informaion/team members informaion
    """    
    context = {} 
    is_pres_referee, is_not_pres_referee, startup, is_operational = informaion_instance_service(startup_id, request.user, context, request.track_info)
    if request.method == 'POST':
        form = request.POST
        if informaion_select_leader_service(form, startup, request.track_info):
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        if informaion_select_not_pres_referee_service(form, startup, request.track_info):
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        if informaion_select_pres_referee_service(form, startup, request.track_info):
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        if information_request_money_service(form, startup, request.track_info, request.user):
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        pres_referee_score = information_pres_referee_score_service(request.user, form, is_pres_referee, startup, request.track_info, is_operational)
        if pres_referee_score == 'pres_referee_score_success':
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(
                    request, f'{pres_referee_score}', extra_tags='pres_referee_form_error')
        not_pres_referee_score = informaion_not_pres_referee_score_service(request.user, form, is_not_pres_referee, startup, request.track_info, is_operational)
        if not_pres_referee_score == 'not_pres_referee_score_success':
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(
                    request, f'{not_pres_referee_score}', extra_tags='not_pres_referee_form_error')
    return render(request, 'startup/information.html', context)


@logging_view
@login_required(login_url='usercp:login')
@premession(th_type1='manager',  role=['operational', 'leader', 'financial'])
# @user_tracker()
def manage_request(request):
    """all of the Requests from all startups that requested money will be shown here

    Arguments:
        request {REQUEST} -- to difine method and track user

    Returns:
        RENDER -- renders mange-request html file
    """    
    
    if request.method == "POST":
        form = request.POST
        if manage_request_service(form, request.track_info):
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    return render(request, 'startup/manage-request.html', manage_request_instance_service())


# @user_tracker(model='requests')
def pop_up(request, requests_id):
    """pop up page for manage request money allow leaders and finances to vote for startup requested money
    
    Arguments:
        request {request} -- pass as context to popups html file
        id {INT} -- is the id of specifi request in Request records
    
    Returns:
        DICT -- returns requestd record and id of the Request object
    """
    if request.method == "GET":
        return render(request, 'startup/popups.html', {'reque': popup_request_service(requests_id)})
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@logging_view
@login_required(login_url='usercp:login')
@premession(th_type1='manager', th_type2='startup', role=['operational', ])
def request_money(request):
    """show the requests money to user depends on requested user role

    Arguments:
        request {REQUEST} -- for requested user and track user

    Returns:
        RENDER -- renders the requests on request-money html file
    """    
    if request.user.user_type == 'startup' and request.user.startup.credit == None:
        return HttpResponseRedirect(request.META.get("HTTP_REFEREE"))
    return render(request, 'startup/request-money.html', request_manage_service(request.user, request.track_info))


@login_required(login_url='usercp:login')
# @user_tracker()
def send_request_money(request):
    """send new request money by ajax request

    Arguments:
        request {REQUEST} -- to check if the request is ajax and define user and track user

    Returns:
        HTTPRESPONSEREDIRECT -- redirect the user at where he/she were if request is not ajax
    """    
    if request.is_ajax():
        form = request.POST
        send_request_money_service(form, request.user, request.track_info)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))



@logging_view
@login_required(login_url='usercp:login')
def single_requestmoney(request, requests_id):
    """the detail of Requests object

    Arguments:
        request {REQUEST} -- to pass to tempalte
        id {INT} -- the id of selected request money

    Returns:
        RENDER -- renders the object of Requsets in single-requestmoney html file
    """    
    the_request = popup_request_service(requests_id)
    return render(request, 'startup/single-requestmoney.html', {'the_request': the_request})


@logging_view
@login_required(login_url='usercp:login')
@premession(th_type1='manager', th_type2='startup', role=['operational', ])
def my_startup_information(request):
    """startup owner can see the informaions of his startup

    Arguments:
        request {REQUEST} -- to define user

    Returns:
        RENDER -- renders mystartup-informaion html file
    """    
    return render(request, 'startup/mystartup-informaion.html', {'startup': get_startup_service(owner=request.user)})


@logging_view
@login_required(login_url='usercp:login')
@premession(th_type1='manager', role=['operational', ])
def remove_referee_form_startup(request):
    """allow operational to remove specific refree from selected startup

    Arguments:
        request {REQUEST} -- to check if request is ajax and get satrtup id and referee id

    Returns:
        HTTPRESPONSEREDIRECT -- redirect the user to where he/she were 
    """    
    if request.is_ajax():
        form = request.POST
        remove_referee_from_startup_service(form, request.track_info)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))



@logging_view
@login_required(login_url='usercp:login')
@premession(th_type1='manager', role=['operational', ])
def can_score_again(request):
    """allow operational to let specific referee for selected startup to rescore the startup

    Arguments:
        request {REQUEST} -- to check if request is ajax and get satrtup id and referee id

    Returns:
        HTTPRESPONSEREDIRECT -- redirect the user to where he/she were 
    """    
    if request.is_ajax():
        form = request.POST
        can_score_again_service(form, request.track_info)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))



# def send_notification_premession(request):
#     if request.is_ajax():
#         form = request.POST
#         startup_comment_id = form.get('startup_c_id')
#         level = form.get('level')
#         referee_ids = form.get('referee_ids')
#         no_referee_ids = form.get('no_referee_ids')
#         document_comments = form.get('document_comments')
#         admin_comment = form.get('admin_comment')
#         modir_comment = form.get('modir_comment')
#         presence_comment = form.get('presence_comment')
#         data = {
#             'startup_c_id': startup_comment_id,
#             'level': level,
#             'referee_ids': referee_ids,
#             'no_referee_ids': no_referee_ids,
#             'document_comments': document_comments,
#             'admin_comment': admin_comment,
#             "modir_comment": modir_comment,
#             "presence_comment": presence_comment,
#         }
#         st_c = models.StartupComments.objects.get(pk=startup_comment_id)
#         to = str(st_c.startup.owner.email)
#         template = 'email/startup-email.html'
#         if level == 'document_comment':
#             if st_c.doc_stat_status  == 'accepted':
#                 sub, the_message = 'صحت مدارک تیم شما توسط ارزیاب اولیه تایید شد. مراحل بعدی به شما اطلاع رسانی خواهد شد', str(
#                     document_comments)
#                 create_notification(st_c.startup.owner, 'accept-document', st_c.startup)
#             elif st_c.doc_stat_status  == 'failed':
#                 sub, the_message = 'صحت مدارک تیم شما توسط ارزیاب اولیه رد شد. لطفا نسبت به تکمیل اطلاعات خود اقدام نمایید', str(
#                     document_comments)
#                 create_notification(st_c.startup.owner, 'fail-document', st_c.startup)

#         elif level == 'startup_stat':
#             if st_c.startup_stat_status == 'accepted':
#                 sub = 'وضعیت طرح ارسالی شما در صد استارتاپ : تایید شده توسط ارزیاب اولیه'
#                 the_message = admin_comment
#                 create_notification(st_c.startup.owner, 'accept-first', st_c.startup)
#             elif st_c.startup_stat_status == 'failed':
#                 sub, the_message = 'وضعیت طرح ارسالی شما در صد استارتاپ :رد شده توسط ارزیاب اولیه', str(
#                     admin_comment)
#                 create_notification(st_c.startup.owner, 'fail-first', st_c.startup)
#         elif level == 'not_presence_referee_notificaion':
#             if st_c.no_referee_stat_status == 'accepted':
#                 sub, the_message = 'تایید داوری غیر حضوری شده توسط مدیر عملیاتی', str(
#                     modir_comment)
#                 create_notification(st_c.startup.owner, 'accept-first_referee', st_c.startup)
#             elif st_c.no_referee_stat_status == 'failed':
#                 sub, the_message = 'رد داوری غیر حضوری شده توسط مدیر عملیاتی', str(
#                     modir_comment)
#                 create_notification(st_c.startup.owner, 'fail-first_referee', st_c.startup)

#         elif level == 'presence_referee_notification':
#             if st_c.referee_stat_status == 'accepted':
#                 sub, the_message = ' تایید داوری حضوری شده توسط مدیر عملیاتی', str(
#                     presence_comment)
#                 create_notification(st_c.startup.owner, 'accept-presence', st_c.startup)
#                 Thread(target=send_email, args=(request,), kwargs={
#                     "to": to , 'template': template, 'sub': sub, 'the_messages': the_message}).start()

#             elif st_c.referee_stat_status == 'failed':
#                 sub, the_message = 'رد داوری حضوری شده توسط مدیر عملیاتی', str(
#                     presence_comment)
#                 create_notification(st_c.startup.owner, 'fail-presence', st_c.startup)
#                 Thread(target=send_email, args=(request,), kwargs={
#                     "to": to , 'template': template, 'sub': sub, 'the_messages': the_message}).start()

#         elif level == 'companion_notification':
#             create_notification(st_c.startup.rahbar, 'select-leader', st_c.startup)
#             create_notification(st_c.startup.owner, 'select-leader', st_c.startup.rahbar)
#         elif level == 'companionra_notification':
#             shetab = models.ShetabDahande.objects.get(
#                 pk='companionra_id')
#             create_notification(st_c.startup.owner, 'selected-as-accelerator', shetab.name_namayande.first())
#             create_notification(shetab.name_namayande.first(), 'selected-as-accelerator', st_c.startup)
#         elif level == 'referee_notification':
#             for referee in Referee.objects.filter(pk__in=no_referee_ids):
#                 create_notification(referee, 'select-not-presence-referees', st_c.startup)
#                 create_notification(st_c.startup.owner, 'select-not-presence-referees', referee)
#         elif level == 'pres_referee_notification':
#             for referee in Referee.objects.filter(pk__in=referee_ids):
#                 create_notification(referee, 'select-presence-referees', st_c.startup)
#                 create_notification(st_c.startup.owner, 'select-presence-referees', referee)
#         try:
#             Thread(target=send_email, args=(request,), kwargs={
#                 "to": to , 'template': template, 'sub': sub, 'the_messages': the_message}).start()
#         except:
#             pass
#         return JsonResponse(data)
#     return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

