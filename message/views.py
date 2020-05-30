from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from urllib.parse import urlsplit
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from . import models
from usercp.models import User, Role
from startup.models import Referee, StartUp
from theevent.models import LeaderModel
from usertracker.models import UserTracker
from django.core.paginator import Paginator
from message.forms import SupportForm, SendMessageForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from threading import Thread
from startups.utils import get_client_ip, premession, logging_view, status_of_user, send_email
from .services import *
import logging
import re

logger = logging.getLogger(__name__)


@logging_view
@login_required(login_url='usercp:login')
# @user_tracker(model='sendmessage')
def send_message_chat(request, user_id):
    """allow user to send message to specific user

    Arguments:
        request {REQUEST} -- to check if request is ajax and for get entered title
        id {INT} -- the id of the receiver user

    Returns:
        RENDER -- rendres the send-message html file with reciever and all message that sent to receiver
    """
    context = {}
    receiver = send_message_chat_instances_service(user_id, request.track_info, context)
    if request.is_ajax():
        form = request.POST
        send = send_message_chat_service(form, request.user, receiver, request.track_info)
        if send == True:
            return redirect('message:message_box')
        else:
            return JsonResponse(send)
    return render(request, 'message/send-message.html', context)


@logging_view
@login_required(login_url='usercp:login')
# @user_tracker(model='sendmessage')
def show_messages(request, allmessages_id):
    """show the selected message and allow user to reply to the message

    Arguments:
        request {REQUEST} -- to define user and track user and get entered values
        id {INT} -- the id of message that want to see and replay

    Returns:
        RENDER -- rendres the show-messages html file
    """    
    context = {}
    the_m = show_messages_instance_service(allmessages_id, request.user, context)
    if request.is_ajax():
        form = request.POST
        message_form = show_message_send_service(form, request.user, request.track_info, the_m)
        if message_form != True:
            messages.error(request, f'{message_form}',
                           extra_tags='request_money_form_error')

    return render(request, 'message/show-messages.html', context)


@logging_view
@login_required(login_url='usercp:login')
# @user_tracker()
def send_message_error(request):
    """allow all users to send fidback to manager

    Arguments:
        request {REQUEST} -- to check if request is ajax and get entered values

    Returns:
        JSONRESPONSE -- returns errors of form if form is not valid
    """    
    receiver = send_message_error_instance_service()
    if request.is_ajax():
        form = request.POST
        current_path = request.META.get('HTTP_REFERER')
        url = ''.join([str(current_path)])
        send = send_message_error_service(form, request.user, url, request.track_info, receiver)
        if send != True:
            messages.error(request, f'{send}')
            return JsonResponse(send)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@logging_view
@login_required(login_url='usercp:login')
# @user_tracker()
def notification(request):
    """list of all notifications for the requested user

    Arguments:
        request {REQUEST} -- to get page number define user and track user

    Returns:
        RENDER -- renders notification html file
    """    
    offset = request.GET.get('page')
    return render(request, 'message/notification.html', notification_service(request.track_info, request.user, offset))


@logging_view
@login_required(login_url='usercp:login')
# @user_tracker()
def message_box(request):
    """all the messages for the requested user
       searchable by startup title , first name user and last name user
    Arguments:
        request {REQUEST} -- to get entered values for search 

    Returns:
        RENDER -- renders message-box html file
    """    
    context = {}
    search = {
    'startup_search': request.GET.get('startup_search'),
    'fname_search': request.GET.get('fname_search'),
    'lname_search': request.GET.get('lname_search'),
    'email_search': request.GET.get('email_search'),
    }
    message_box_service(request.track_info, search, context)
    return render(request, 'message/message-box.html', context)


@logging_view
def support_msg(request):
    """the startup owner can send error fidbacke this fidback will be send as email to support staff 

    Arguments:
        request {REQUEST} -- to define method and get image-base-64 and ajax request

    Returns:
        HTTPRESPONSEREDIRECT -- redirect user to where he/she were if request is not ajax
    """    
    if request.method == "POST":
        form = request.POST
        file_value = request.FILES
        protocol = urlsplit(request.build_absolute_uri(None)).scheme
        current_site = get_current_site(request)
        support_form = support_service(request.user, file_value, form, request.session, request.track_info, current_site, protocol)
        if support_form != True:
            messages.error(request, f'{support_form}')
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))