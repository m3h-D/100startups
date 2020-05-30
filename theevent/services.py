from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction
from persiantools.jdatetime import JalaliDate, JalaliDateTime
from startups.utils import *
from startups.object import get_startup_service
from startup.models import *
from . import models
from usercp.models import User
from startups.object import get_user_service, get_create_event_service
import re



@transaction.atomic
def offerto_leader_service(owner, form, track_info):
    """create an event with the type of leader
       - get the list of leaders ids and assgin CreateEvent by their model and id (GenericForeignKey)
         and then assgin them to TheEvent object
       - get the list of startups ids and create LeaderModel object with user model assgin to it(the choosen leader)
    
    Arguments:
        owner {OBJECT} -- requested user (the maker of this event)
        form {POST Method} -- to get ids from the maker
    
    Returns:
        BOOLEAN -- returns True if everything goes well
    """
    the_event = models.TheEvent.objects.create(
        owner=owner, th_type='leader')
    if form.getlist('leader[]'):
        for person_id in form.getlist('leader[]'):
            if not re.search(r'\d', person_id, re.I): continue
            user_leader = get_user_service(pk=int(person_id))
            event = models.CreateEvent.objects.create_by_model(
                instance=user_leader,
            )
            the_event.c_event.add(event)
            the_event.save()
            for st in form.getlist(f'startup-{person_id}'):
                if not re.search(r'\d', st, re.I):
                    continue
                startup = get_startup_service(pk=int(st))
                models.LeaderModel.objects.create(
                    event=event,
                    startup=startup,
                )
                status = f"استارتاپ {startup.title} به راهبر {user_leader} پیشنهاد داده شد"
                status_of_user(track_info, status, 'assigne-startup-to-leader')
                create_notification(startup.owner, 'assigne-startup-to-leader', user_leader)
                create_notification(user_leader, 'assigne-startup-to-leader', startup)
        return True


def offerto_leader_list_service(get_page, track_info):
    """list all offer to leaders startup by date
    
    Arguments:
        get_page {GET Method} -- get the page number
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
    
    Returns:
        DICT -- returns querysets of TheEvent model that has the type of leader
    """
    status = f"لیست استارت اپ های پیشنهاد شده به راهبران را دید"
    status_of_user(track_info, status, 'import-offerto-leader-list')
    offers = models.TheEvent.objects.prefetch_related('c_event', 'startuptime').select_related('owner').filter(th_type='leader').order_by('-created_date')
    paginator = Paginator(offers, 30)
    page = get_page.get('page')
    offers = paginator.get_page(page)
    return {'offers': offers, 'page': page}



def edit_offerto_leader_events(id):
    """get the TheEvent object by the given id

    Arguments:
        id {INT} -- the id of TheEvent object

    Returns:
        TUPLE -- returns a tuple of TheEvent object and a queryset of CreateEvent
    """    
    the_event = models.TheEvent.objects.prefetch_related('c_event').get(pk=id)
    all_events = models.CreateEvent.objects.prefetch_related('theevent_leadermodel').filter(
        theevent=the_event,
    )
    return the_event, all_events

@transaction.atomic
def edit_offerto_leader_get_create(form, the_event, track_info):
    """update or create the LeaderModel and CreateEvent records

    Arguments:
        form {POST Method} -- to get new entered values
        the_event {OBJECT} -- TheEvent objecte that got by id
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        BOOLEAN -- returns True if everything goes well
    """    
    if form.getlist('leader[]'):
        create_event_id = (c_e for c_e in form.getlist('c_e_id'))
        for person_id in form.getlist('leader[]'):
            if not re.search(r'\d', person_id, re.I): continue
            leader_id = (c_e for c_e in form.getlist(f'lead_pk-{person_id}'))
            user_leader = get_user_service(pk=int(person_id))
            try:
                event = get_create_event_service(pk=int(create_event_id.__next__()))
                event.content_object = user_leader
                event.save()
            except:
                event = models.CreateEvent.objects.create_by_model(instance=user_leader)
            finally:
                the_event.c_event.add(event)
                the_event.save()
                
                for st in form.getlist(f'startup-{person_id}'):
                    if not re.search(r'\d', st, re.I): continue
                    start = get_startup_service(pk=int(st))
                    try:
                        leader = models.LeaderModel.objects.get(pk=int(leader_id.__next__()))
                        leader.startup = start
                        leader.save()
                    except:
                        models.LeaderModel.objects.create(
                            event=event,
                            startup=start,
                        )

                    status = f"ملاقات {the_event.pk} با راهبر {user_leader.first_name} {user_leader.last_name} به استارتاپ {get_startup_service(pk=int(st)).title} تغییر کرد"
                    status_of_user(track_info, status, 'edit-offerto-leader')
                    create_notification(user_leader, 'edit-offerto-leader', start)
                    create_notification(start.owner, 'edit-offerto-leader', user_leader)
    return True

@transaction.atomic
def meeting_coach_service(form, owner, track_info):
    """create new event with type of coach

    Arguments:
        form {POST Method} -- to get entered values
        owner {OBJECT} -- the maker of this event
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        BOOLEAN -- returns True if everything goes well
    """
    if form.getlist('coach[]'):
        the_event = models.TheEvent.objects.create(
            owner=owner, th_type='coach')
        for person_id in form.getlist('coach[]'):
            if not person_id:
                continue
            user_inv = User.objects.filter(
                pk=int(person_id)).first()
            event = models.CreateEvent.objects.create_by_model(
                instance=user_inv,
            )
            the_event.c_event.add(event)
            the_event.save()
            for x in range(len(form.getlist(f'meeting-{person_id}'))):
                if form.getlist(f'meeting-{person_id}')[x] == u"انتخاب": continue
                try:
                    schedule, created = models.StartupTime.objects.get_or_create(the_event=the_event,
                                                                the_date=datetime.fromtimestamp(
                                                                        float(form.get('date_meeting_s'))/1000),
                                                                to_date=datetime.fromtimestamp(
                                                                        float(form.get('date_meeting_e'))/1000),
                                                                from_time=datetime.fromtimestamp(
                                                                        float(form.getlist('meeting_time_s')[x])/1000),
                                                                to_time=datetime.fromtimestamp(
                                                                        float(form.getlist('meeting_time_e')[x])/1000),
                                                                )
                    models.CoachEvent.objects.create(event=event,
                                                    schedule=schedule,
                                                    th_time=int(form.getlist(f'meeting-{person_id}')[x]))

                except Exception as e:
                    logger.error(str(e))
                    print(str(e))
            status = f"یک ملاقات برای مربی {user_inv.first_name} {user_inv.last_name} ایجاد کرد"
            status_of_user(track_info, status, 'create-meetingto-coach')
            create_notification(user_inv, 'create-meetingto-coach', user_inv)

    return True


def edit_meeting_event_service(id):
    """get TheEvent by given id

    Arguments:
        id {INT} -- id of TheEvent object

    Returns:
        TUPLE -- returns tuple of TheEvent object and CreateEvent queryset
    """    
    the_event = models.TheEvent.objects.prefetch_related('c_event', 'startuptime').get(pk=id)
    all_events = models.CreateEvent.objects.prefetch_related('theevent_coachevent').filter(
        theevent=the_event,
    )
    return the_event, all_events

@transaction.atomic
def edit_meeting_get_create_service(form, the_event, track_info):
    """get the event and coach id to update if there is instances else create new

    Arguments:
        form {POST Method} -- to get entered values
        the_event {OBJECT} -- TheEvent object that got by id
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        BOOLEAN -- returns True if everything goes well
    """    
    if form.getlist('coach[]'):
        create_event_id = (c_e for c_e in form.getlist('c_e_id'))
        for person_id in form.getlist('coach[]'):
            if not person_id: continue
            coach_id = (c_e for c_e in form.getlist(f'coach_pk-{person_id}'))
            startuptime_id = (sut for sut in form.getlist('startuptime'))
            from_time = (ft for ft in form.getlist('meeting_time_s'))
            to_time = (tt for tt in form.getlist('meeting_time_e'))
            from_date = form.get('date_meeting_s')
            to_date = form.get('date_meeting_e')
            user_coach = get_user_service(pk=int(person_id))
            try:
                event = get_create_event_service(pk=int(create_event_id.__next__()))
                event.content_object = user_coach
                event.save()
            except:
                event = models.CreateEvent.objects.create_by_model(instance=user_coach)
            finally:
                the_event.c_event.add(event)
                the_event.save()

            for th in form.getlist(f'meeting-{person_id}'):
                if not re.search(r'\d', th, re.I): continue
                try:
                    times = models.StartupTime.objects.get(pk=startuptime_id.__next__())
                    times.the_date = datetime.fromtimestamp(float(from_date)/1000)
                    times.to_date = datetime.fromtimestamp(float(to_date)/1000)
                    times.from_time = datetime.fromtimestamp(float(from_time.__next__())/1000)
                    times.to_time = datetime.fromtimestamp(float(to_time.__next__())/1000)
                    times.save()
                                            
                except:
                    times = models.StartupTime.objects.create(the_event=the_event,
                                                                the_date=datetime.fromtimestamp(float(from_date)/1000),
                                                                to_date=datetime.fromtimestamp(float(to_date)/1000),
                                                                from_time=datetime.fromtimestamp(float(from_time.__next__())/1000),
                                                                to_time=datetime.fromtimestamp(float(to_time.__next__())/1000),
                                                                )                          
                finally:
                    try:
                        start_events = models.CoachEvent.objects.get(pk=int(coach_id.__next__()))

                        start_events.th_time = th
                        start_events.schedule = times
                        start_events.save()
                    except:
                        start_events = models.CoachEvent.objects.create(event=event, schedule=times, th_time=int(th))
                        
                    status = f"منتورینگ {the_event.id} با مربی {user_coach.first_name} {user_coach.last_name} به وضعیت {'آزاد' if start_events.th_time == 1 else 'پر'} و تاریخ {JalaliDate.to_jalali(times.the_date.year, times.the_date.month, times.the_date.day)} تا {JalaliDate.to_jalali(times.to_date.year, times.to_date.month, times.to_date.day)} و زمان {times.from_time} تا {times.to_time} تغییر کرد"
                    status_of_user(track_info, status, 'edit-meetingto-coach')
                    create_notification(user_coach, 'edit-meetingto-coach', start_events)
        return True


def list_meeting_service(track_info):
    """show list of events that has th type of coach

    Arguments:
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        DICT -- returns dictionary of TheEvent object
    """    
    status = f"لیست ملاقات مربیان را دید"
    status_of_user(track_info, status, 'import-meetingto-coach-list')
    meetings = models.TheEvent.objects.prefetch_related('c_event', 'startuptime').select_related('owner').filter(
        th_type='coach').order_by('-created_date')
    return {'meetings': meetings, }


def edit_create_event_service(id):
    """get TheEvent by id and type of investor to edit

    Arguments:
        id {INT} -- the id of TheEvent object

    Returns:
        TUPLE -- returns tuple of CreateEvent queryset and TheEvent object
    """
    the_event = models.TheEvent.objects.prefetch_related('c_event', 'startuptime').get(pk=id, th_type='investor')
    all_events = models.CreateEvent.objects.filter(
        theevent=the_event,
    )
    return the_event, all_events

@transaction.atomic
def edit_get_create_event(the_event, form, track_info):
    """get the id of CreateEvent object and StartupEvent and StartupTime if there is instances and update it else create new

    Arguments:
        the_event {OBJECT} -- to add new CreateEvents to TheEvent object
        form {POST Method} -- to get entred values
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        BOOLEAN -- returns True if everything goes well
    """    
    create_event_id = (c_e for c_e in form.getlist('c_e_id'))
    if form.getlist('investor[]'):
        for person_id in form.getlist('investor[]'):
            if not person_id: continue
            startup_event = (s_e for s_e in form.getlist('startup_event_id'))
            the_date = (s_d for s_d in form.getlist('date_meeting'))
            from_time = (f_t for f_t in form.getlist('meeting_time_s'))
            to_time = (t_t for t_t in form.getlist('meeting_time_e'))
            startuptime_id = (sut for sut in form.getlist('startuptime'))
            user_inv = Investors.objects.filter(
                user__pk=int(person_id))
            try:
                event = get_create_event_service(pk=int(create_event_id.__next__()))
                event.content_object = user_inv
                event.save()
            except:
                event = models.CreateEvent.objects.create_by_model(instance=user_inv)
            finally:
                the_event.c_event.add(event)
                the_event.save()

            for startup_id in form.getlist(f'startup-{person_id}'):
                if not re.search(r'\d', startup_id, re.I): continue
                startup = get_startup_service(pk=int(startup_id))

                try:
                    times = models.StartupTime.objects.get(pk=startuptime_id.__next__())
                    times.the_date = datetime.fromtimestamp(float(the_date.__next__())/1000)
                    times.from_time = datetime.fromtimestamp(float(from_time.__next__())/1000)
                    times.to_time = datetime.fromtimestamp(float(to_time.__next__())/1000)
                    times.save()
                                        
                except:
                    models.StartupTime.objects.create(the_event=the_event,
                                                    the_date=datetime.fromtimestamp(float(the_date.__next__())/1000),
                                                    from_time=datetime.fromtimestamp(float(from_time.__next__())/1000),
                                                    to_time=datetime.fromtimestamp(float(to_time.__next__())/1000),
                                                    )
                finally:
                    try:
                        start_events = models.models.StartupsEvent.objects.get(pk=int(startup_event.__next__()))
                        start_events.schedule = times
                        start_events.save()
                    except:
                        start_events = models.models.StartupsEvent.objects.create(event=event, schedule=times, startup=startup)

                    try:
                        status = f"برای سرمایه گذار {event.investor.user.first_name} {event.investor.user.last_name} یک ایونت برای استارت اپ {startup} بروزرسانی کرد"
                        status_of_user(track_info, status)
                        create_notification(event.investor.user, 'create-event-investor', startup)
                        create_notification(startup.owner, 'create-event-investor', event.investor.user)

                    except:
                        pass
    return True

@transaction.atomic
def create_event_service(form, owner, track_info):
    """create new event with type of investor and get the user throw Investor user id

    Arguments:
        form {POST Method} -- get entered values
        owner {OBJECT} -- requested user to define the maker
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        BOOLEAN -- returns True if everything goes well
    """    
    the_event = models.TheEvent.objects.create(
        owner=owner, th_type='investor')

    if form.getlist('investor[]'):
        for person_id in form.getlist('investor[]'):
            if not person_id:
                continue
            user_inv = Investors.objects.filter(
                user__pk=int(person_id)).first()
            event = models.CreateEvent.objects.create_by_model(
                instance=user_inv
            )
            the_event.c_event.add(event)
            the_event.save()
            for x in range(len(form.getlist(f'startup-{person_id}'))):
                if not re.search(r'\d', form.getlist(f'startup-{person_id}')[x], re.I): continue

                # try:
                schedule, created = models.StartupTime.objects.get_or_create(the_event=the_event,
                                                            the_date=datetime.fromtimestamp(
                                                                                float(form.getlist('date_meeting')[x])/1000),
                                                            from_time=datetime.fromtimestamp(
                                                                                float(form.getlist('meeting_time_s')[x])/1000),
                                                            to_time=datetime.fromtimestamp(
                                                                                float(form.getlist('meeting_time_e')[x])/1000))
                models.StartupsEvent.objects.create(event=event,
                                                    startup=get_startup_service(pk=int(form.getlist(f'startup-{person_id}')[x])),
                                                    schedule=schedule)

                # except:
                #     pass

                try:
                    status = f"برای سرمایه گذار {event.investor.user.first_name} {event.investor.user.last_name} برای استارت اپ {startup} ایونت ساخت"
                    status_of_user(track_info, status, 'create-event-investor')
                    create_notification(event.investor.user, 'create-event-investor', startup)
                    create_notification(startup.owner, 'create-event-investor', event.investor.user)
                except:
                    pass

    return True


def list_event_service(offset, track_info):
    """list of investor events

    Arguments:
        offset {GET Method} -- to set pagination
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        DICT -- returns dictionary of events queryset and page number
    """    
    status = f"لیست ایونت ها را دید"
    status_of_user(track_info, status, 'import-list-events')
    events = models.TheEvent.objects.prefetch_related('c_event', 'startuptime').select_related('owner').filter(
        th_type='investor').order_by('-created_date')
    paginator = Paginator(events, 30)
    page = offset.get('page')
    events = paginator.get_page(page)
    return {"events": events, 'page': page}





def add_to_leader_service(ajax_data, track_info):
    """allow leader to accpet to meet the offered startup

    Arguments:
        ajax_data {DICT} -- contains LeaderModel instance id
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        DICT -- returns dictionary of leadermodel id
    """    
    stat_id = ajax_data.get('stat_id')
    data = {
        'startup_id': stat_id,
    }
    try:
        te_leader = models.LeaderModel.objects.get(pk=stat_id)
        if te_leader.status == 1:
            te_leader.status = 0
            te_leader.save()
            try:
                status = f"{te_leader.user.first_name} {te_leader.user.last_name} راهبری استارت اپ {te_leader.startup.title} را رد کرد"
                status_of_user(track_info, status, 'not-wants-to-meet-startup')
                create_notification(te_leader.startup.owner, 'not-wants-to-meet-startup', te_leader.user)
            except:
                pass

        elif te_leader.status == 0:
            te_leader.status = 1
            te_leader.save()
            try:
                status = f"{te_leader.user.first_name} {te_leader.user.last_name} راهبری استارت اپ {te_leader.startup.title} را قبول کرد"
                status_of_user(track_info, status, 'wants-to-meet-startup')
                create_notification(te_leader.startup.owner, 'wants-to-meet-startup', te_leader.user)
            except:
                pass
    except Exception as e:
        logger.error(str(e))
    return data


def wants_to_meet_service(owner, track_info, ajax_data):
    """allow startup to reserve a time to meet coaches

    Arguments:
        owner {OBJECT} -- requested user that own a startup
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
        ajax_data {DICT} -- a dictionary that contains create event id and TheEvent id and CoachEvent id to ensuer that every startup can only reserve 2 meeting every event

    Returns:
        DICT -- returns dictionary of data for ajax
    """    
    data = {
        'meeting_id': ajax_data.get('c_id'),
        'coach_id': ajax_data.get('coach_id'),
        'the_event': ajax_data.get('th_pk'),
    }
    th_startup = get_startup_service(owner=owner)
    cat = get_create_event_service(pk=ajax_data.get('coach_id'))
    the_event = models.TheEvent.objects.get(pk=ajax_data.get('th_pk'))
    try:
        wants = models.WantsMeet.objects.get(the_event=the_event)
        wants.event_counter += 1
        wants.save()
    except:
        wants = models.WantsMeet.objects.create(
            the_event=the_event, startup=th_startup, c_event=cat)

    status = f"استارتاپ {th_startup.title} تمایل به رزرو وقت با مربی {cat.content_object.first_name} {cat.content_object.last_name} دارد"
    status_of_user(track_info, status, 'assigne-startup-to-leader')
    create_notification(th_startup.owner, 'assigne-startup-to-leader', cat.content_object)
    create_notification(cat.content_object, 'assigne-startup-to-leader', th_startup)

    coach = models.CoachEvent.objects.get(pk=ajax_data.get('c_id'))
    coach.startup = th_startup
    coach.th_time = 2
    coach.save()
    return data