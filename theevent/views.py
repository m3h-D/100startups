from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from datetime import datetime
from . import models
from usercp.models import Role, User
from startup.models import StartUp, Investors
from usertracker.models import UserTracker
from .services import *
from startups.utils import get_client_ip, premession, logging_view, status_of_user, get_list, get_list2, create_notification
import logging
import re


logger = logging.getLogger(__name__)
# Create your views here.


@logging_view
@login_required(login_url='usercp:login')
@premession(th_type1='manager', role=['operational', ])
# @user_tracker()
def offerto_leader(request):
    """the operational can offer startups that have no rahbar_asli to leaders

    Arguments:
        request {REQUEST} -- to define who is making this event

    Returns:
        RENDER -- renders the offerto-leader html file
    """    
    if request.method == "POST":
        form = request.POST
        try:
            offerto_leader_service(request.user, form, request.track_info)
            return redirect('theevent:list_offer')
        except Exception as e:
            logger.error(str(e))

    return render(request, 'theevent/offerto-leader.html')



@logging_view
@login_required(login_url='usercp:login')
@premession(th_type1='manager', role=['operational', ])
# @user_tracker()
def list_offer(request):
    """list of leaders that startups are assign to them

    Arguments:
        request {GET Method} -- to do some pagination

    Returns:
        QUERYSET -- return squeryset of TheEvent
    """    
    get_page = request.GET
    return render(request, 'theevent/list-offer.html', offerto_leader_list_service(get_page, request.track_info))



@logging_view
@login_required(login_url='usercp:login')
@premession(th_type1='manager', role=['operational', ])
# @user_tracker(model='theevent')
def edit_offer_to_leader(request, theevent_id):
    """allow operationals to edit offer to leader events

    Arguments:
        request {POST Method} -- to get new valuse from user
        id {INT} -- the id of the TheEvent that operationals try to edit

    Returns:
        RENDER -- renders the offertoleader-edit html file
    """    
    the_event, all_events = edit_offerto_leader_events(theevent_id)
    if request.method == "POST":
        form = request.POST
        edit_offerto_leader_get_create(form, the_event, request.track_info)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    return render(request, 'theevent/offerleader-edit.html', {'leaders': all_events})



@logging_view
@login_required(login_url='usercp:login')
@premession(th_type1='manager', role=['operational', ])
# @user_tracker()
def list_meeting(request):
    """show the list of mentoring events

    Arguments:
        request {REQUEST} -- to pass to template as primary context and track user

    Returns:
        RENDERS -- renders a queryset of mentoring event
    """    
    
    return render(request, 'theevent/list-meeting.html', list_meeting_service(request.track_info))



@logging_view
@login_required(login_url='usercp:login')
@premession(th_type1='manager', role=['operational', ])
# @user_tracker(model='theevent')
def edit_meeting_coach(request, theevent_id):
    """allow operationals to edit the mentoring event

    Arguments:
        request {REQUEST} -- to define post method and track user
        theevent_id {INT} -- the id of the event that operational trying to edit

    Returns:
        RENDER -- renders a querysets of TheEvent and CreatEvent to show the specifications of the event
    """    
    the_event, all_events = edit_meeting_event_service(theevent_id)
    if request.method == "POST":
        form = request.POST
        edit_meeting_get_create_service(form, the_event, request.track_info)
        return redirect('theevent:list_meeting')

    return render(request, 'theevent/meeting-edit.html', {'the_event': the_event, 'all_events': all_events})




@logging_view
@login_required(login_url='usercp:login')
def wants_to_meet(request):
    
    if request.is_ajax():
        ajax_data ={
            "c_id": request.POST.get('meeting_id'),
            "coach_id": request.POST.get('coach_id'),
            "th_pk": request.POST.get('the_event'),
        }
        return JsonResponse(wants_to_meet_service(request.user, request.track_info, ajax_data))
    return HttpResponseRedirect(request.META.get("HTTP_REFEREE"))



@logging_view
@login_required(login_url='usercp:login')
@premession(th_type1='manager', role=['operational', ])
# @user_tracker()
def meeting_coach(request):
    """allow operational to create schedulation for coaches

    Arguments:
        request {REQUEST} -- to define method as POST and define the maker of event and track user

    Returns:
        RENDER -- renders the meetingto-coach html file
    """    
    if request.method == "POST":
        form = request.POST
        meeting_coach_service(form, request.user, request.track_info)
        return redirect('theevent:list_meeting')
    return render(request, 'theevent/meetingto-coach.html')


@logging_view
@login_required(login_url='usercp:login')
@premession(th_type1='manager', role=['operational', ])
# @user_tracker()
def create_event(request):
    """allow operationals to create events for investors that accepted some startups that have status of add_to_invest for invest

    Arguments:
        request {REQUEST} -- to define the method as POST and define the maker of event and track user

    Returns:
        RENDER -- renders the create-event html file
    """    
    if request.method == "POST":
        form = request.POST
        create_event_service(form, request.user, request.track_info)
        return redirect('theevent:list_event')
    return render(request, 'theevent/create-event.html')


@logging_view
@login_required(login_url='usercp:login')
@premession(th_type1='manager', role=['operational', ])
# @user_tracker(model='theevent')
def edit_create_event(request, theevent_id):
    """allow operationals to edit the specific invest events

    Arguments:
        request {REQUEST} -- to define method as POST and track the user
        id {INT} -- the id of the TheEvent object that operational wants to edit

    Returns:
        RENDER -- renders the TheEvent object and queryset of CreateEvent
    """    
    the_event, all_events = edit_create_event_service(theevent_id)
    if request.method == "POST":

        form = request.POST
        edit_get_create_event(the_event, form, request.track_info)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    return render(request, 'theevent/edit-event.html', {"the_event": the_event, "all_events": all_events})



@logging_view
@login_required(login_url='usercp:login')
# @user_tracker()
def add_to_leader(request):
    """allow leaders to accept or decline the offered startups to lead

    Arguments:
        request {REQUEST} -- to define method as POST and to request as ajax

    Returns:
        JSONRESPONSE -- returns data as json
    """    
    if request.is_ajax():
        ajax_data = request.POST.get('startups_id')
        return JsonResponse(add_to_leader_service(ajax_data, request.track_info))
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@logging_view
@login_required(login_url='usercp:login')
@premession(th_type1='manager', role=['operational', ])
# @user_tracker()
def list_event(request):
    """list of the investor events

    Arguments:
        request {REQUEST} -- to define method as GET for pagination and track user

    Returns:
        RENDER -- renders queryset of events that assigned investors to startups
    """    
    offset = request.GET
    return render(request, 'theevent/list-event.html', list_event_service(offset, request.track_info))