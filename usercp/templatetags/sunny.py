from django import template
from django.http import HttpResponseRedirect
import pickle
import json
import ast

register = template.Library()




@register.filter(name='ref_nomre')
def ref_nomre(unpickle_nomre):
    """unpicle the scores that referees granted to an startup
    
    Arguments:
        unpickle_nomre {PICKLE} -- a pickle of scores
    
    Returns:
        DICT -- unpickled scores
    """
    try:
        return pickle.loads(unpickle_nomre)
    except Exception as e:
        return str(e)



# @register.simple_tag
# def leader_startups(offer_user):
#     """[summary]
    
#     Arguments:
#         offer_user {[type]} -- [description]
    
#     Yields:
#         [type] -- [description]
#     """
#     from theevent import models
#     offer = models.LeaderModel.objects.filter(user=offer_user)
#     for x in offer:
#         yield x.startup.title


@register.simple_tag
def add_invest(user, startup):
    """checks the status of an investor that assigned to a startup
    
    Arguments:
        user {OBJECT} -- requsted user
        startup {OBJECT} -- selected startup
    
    Returns:
        INT -- returns 1 or 0 based on if investor wants to meet
    """
    from startup import models
    from django.shortcuts import get_object_or_404
    try:
        heh = models.Investors.objects.get(user=user, startup__pk=int(startup))
        return heh.status
    except:
        return 0



@register.simple_tag
def startups_c_event(event):
    """list of startups that been chosen for invesotr
       in create event
    
    Arguments:
        event {OBJECT} -- the event that startup has been chosen
    
    Returns:
        QUERYSET -- returns queryset of startups
    """
    from theevent import models
    return models.StartupsEvent.objects.filter(event=event)



@register.simple_tag
def time_event(event):
    """show all the dates and times that assgin in every event
    
    Arguments:
        event {[type]} -- [description]
    
    Returns:
        QUERYSET -- returns queryset of times that assigned to the event
    """
    from theevent import models
    return models.StartupTime.objects.filter(the_event=event).distinct()    





@register.simple_tag
def time_event_startup(startup):
    """show the time of meeting if accepted
    
    Arguments:
        startup {INT} -- the id of selected startup
    
    Returns:
        OBJECT -- return the startup event
    """
    from theevent import models
    from startups.object import get_startup_service
    try:
        startups = get_startup_service(pk=startup)
        the_time = models.StartupsEvent.objects.filter(startup=startups).distinct()
    except:
        the_time = None
    return the_time   



@register.filter
def check_2_list(model, investor_startup):
    from theevent.models import CreateEvent
    event = CreateEvent.objects.filter(investors__in=investor_startup)
    return model.filter(event__in=event)




@register.simple_tag
def list_counter(count):
    """check how many left to be 8
    
    Arguments:
        count {INT} -- the number that is less than 8
    
    Returns:
        INT -- reutrns minus of 8 and count
    """
    num = 8 - int(count)
    return num 

@register.simple_tag
def list_counter2(count):
    """check how many left to be 4
    
    Arguments:
        count {INT} -- the number that is less than 8
    
    Returns:
        INT -- reutrns minus of 4 and count
    """
    num = 4 - int(count)
    return num 

@register.simple_tag
def list_counter_for(count):
    """add querysets count with forloop to get unique number
    
    Arguments:
        count {INT} -- number of objects in queryset
    
    Returns:
        INT -- return the number that been given
    """
    return count



@register.filter
def request_status(model, status):
    """a custome filter template tag to count objects of specific model 
    
    Arguments:
        model {QUERYSET} -- a queryset of specific model
        status {STRING} -- the status of the model that been given
    
    Returns:
        INT -- returns the number of objects with specified status
    """
    return model.filter(status=status).count()



@register.simple_tag
def count_requests(model, request, status=None):
    """get Request model objects count base on their status 
       and show them by role of requested user
    
    Arguments:
        model {QUERYSET} -- the model that been given to count it's objects
        request {REQUEST} -- to get requested user role
    
    Keyword Arguments:
        status {STRING} -- optional kwarg that will specifie the status (default: {None})
    
    Returns:
        INT -- returns the number of objects with specified status
    """
    from startups.object import get_role_service
    is_op = get_role_service(name='operational')
    if request.user.is_admin or request.user.user_type == 'manager' or is_op in request.user.role.all():
        if status:
            return model.filter(status=status).count()
        return model.count()
    else:
        if status:
            return model.filter(user=request.user,status=status).count()
        return model.filter(user=request.user).count()


@register.filter
def not_readed_notification(model):
    """count the numbers of messages and notifications
    
    Arguments:
        model {QUERYSET} -- the queryset of the given model
    
    Returns:
        INT/STRING -- returns nothing if there is not not readed message else retursn the number of not readed messages
    """
    counter = model.filter(is_readed=False).count()
    return counter if counter != 0 else ''


@register.simple_tag
def get_create_event(th_pk):
    """gets the TheEvent instance and filter CreateEvent models by the insatnce of TheEvent
    
    Arguments:
        th_pk {OBJECT} -- the object of TheEvent Model
    
    Returns:
        QUERYSET -- returns queryset of CreateEvents objects
    """
    from theevent import models
    return models.CreateEvent.objects.filter(theevent=th_pk) 



@register.simple_tag
def get_count_coach(th_pk):
    """count the numbers of startup meeting in every event 
    
    Arguments:
        th_pk {OBJECT} -- object of TheEvent model
    
    Returns:
        NONE/OBJECT -- check if it's exists or not and if there is it's should not be more than 2(it will be checked in template)
    """
    from theevent import models
    try:
        return models.WantsMeet.objects.get(the_event=th_pk)
    except:
        return None



@register.simple_tag
def dashboard_role_counter(role):
    """count the users with specific roles
    
    Arguments:
        role {OBJECT} -- the Role object
    
    Returns:
        INT -- returns number of users with specified role
    """
    from usercp.models import User
    return User.objects.filter(role=role).count()