from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from threading import Thread
from django.core import files
from persiantools.jdatetime import JalaliDate, JalaliDateTime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from . import models
from category.models import Categories
from usercp.forms import LeaderForm, LeaderUserForm
from startups.object import get_user_service, get_role_service, get_startup_service
from theevent.models import LeaderModel
from startups.utils import *
from .forms import *
import re
import pickle
import logging

logger = logging.getLogger(__name__)



def list_startup_service(track_info, offset, search):
    """all startups ordered by created time and searchable

    Arguments:
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
        offset {GET Method} -- to get page number
        search {DICT} -- a dictionary of entered values for search

    Returns:
        DICT -- returns dictionary of contextes
    """    
    status = "لیست استارت اپ ها را دید"
    status_of_user(track_info, status, 'import-list-startup')
    startups = models.StartUp.objects.select_related('owner').all().order_by('-created_date')
    the_startups = startups
    categories = Categories.objects.all()
    if search.get("status"):
        if search.get("status") == 'pending':
            startups = startups.filter(Q(status='pending')|Q(status='editing')).distinct()
        else:
            startups = startups.filter(status=search.get("status"))
        startups = startups.filter(status=search.get("status"))
        the_startups = startups
        try:
            status = f"استارت اپ {startups.first.title} را جستجو کرد"
            status_of_user(track_info, status, 'search-list-startup')
        except:
            pass

    if search.get("province"):
        startups = startups.filter(province_startup=search.get("province"))
        the_startups = startups

    if search.get("city"):
        startups = startups.filter(city_startup=search.get("city"))
        the_startups = startups

    if search.get("name"):
        startups = startups.filter(title__icontains=search.get("name"))
        the_startups = startups
        try:
            status = f"استارت اپ {startups.first.title} را جستجو کرد"
            status_of_user(track_info, status, 'search-list-startup')
        except:
            pass

    if search.get("cat_id"):
        cat = Categories.objects.get(pk=int(search.get("cat_id")))
        startups = startups.filter(category=cat)
        the_startups = startups

    if search.get("lname"):
        startups = startups.filter(owner__last_name__icontains=search.get("lname"))
        the_startups = startups
        try:
            status = f"استارت اپ {startups.first.title} را جستجو کرد"
            status_of_user(track_info, status, 'search-list-startup')
        except:
            pass


    if search.get("shetab"):
        startups = startups.filter(
            shetab_dahande__name_shtabdahande__icontains=search.get("shetab"))
        the_startups = startups
        try:
            status = f"استارت اپ {startups.first.title} را جستجو کرد"
            status_of_user(track_info, status, 'search-list-startup')
        except:
            pass

    if search.get("email"):
        startups = startups.filter(owner__email__icontains=search.get("email"))
        the_startups = startups
        try:
            status = f"استارت اپ {startups.first.title} را جستجو کرد"
            status_of_user(track_info, status, 'search-list-startup')
        except:
            pass


    if search.get("the_phone"):
        startups = startups.filter(owner__phone__icontains=search.get("the_phone"))
        the_startups = startups
        try:
            status = f"استارت اپ {startups.first.title} را جستجو کرد"
            status_of_user(track_info, status, 'search-list-startup')
        except:
            pass

    if search.get("start_date") and search.get("end_date"):
        end_date_lists = get_list(search.get("end_date"))
        e_date = JalaliDate(
            end_date_lists[0], end_date_lists[1], end_date_lists[2]).to_gregorian()
        start_date_lists = get_list(search.get("start_date"))
        s_date = JalaliDate(
            start_date_lists[0], start_date_lists[1], start_date_lists[2]).to_gregorian()
        new_end = e_date + timezone.timedelta(days=1)
        startups = startups.filter(created_date__range=[s_date, new_end])
        the_startups = startups
        try:
            status = f"استارت اپ {startups.first.title} را جستجو کرد"
            status_of_user(track_info, status, 'search-list-startup')
        except:
            pass

    paginator = Paginator(startups, 30)
    page = offset
    startups = paginator.get_page(page)
    return {'startups': startups,
    'page': page,
    'the_startups': the_startups,
    'name': search.get('name'),
    'cat_id': search.get('cat_id'),
    'status': search.get('status'),
    'lname': search.get('lname'),
    'shetab': search.get('shetab'),
    'email': search.get('email'),
    'categories': categories,
    'province': search.get('province'),
    'start_date': search.get('start_date'),
    'end_date': search.get('end_date'),
    'the_phone': search.get('the_phone'),
    'city': search.get('city'), }


def select_startup_service(startup_id, track_info):
    """will make selected field of selected startup True if it's False and vice versa by ajax request

    Arguments:
        startup_id {INT} -- the given id of startup by ajax request
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        JSONRESPONSE -- returns json response for ajax
    """    
    data = {
        'add_id': startup_id
    }
    the_start = get_startup_service(id=startup_id)
    if the_start.selected == True:
        the_start.selected = False
        the_start.save()
        status = f"{the_start.title} را منتخب کرد"
        status_of_user(track_info, status, 'selected-startup')
        create_notification(the_start.owner, 'selected-startup', the_start)
    else:
        the_start.selected = True
        the_start.save()
        status = f"{the_start.title} را از منتخب خارج کرد"

        status_of_user(track_info, status, 'not-selected-startup')
        create_notification(the_start.owner, 'not-selected-startup', the_start)
    return data


def delete_startup_service(startup_id, track_info):
    """delete the specific startup by given id by ajax

    Arguments:
        startup_id {INT} -- the id of selected startup
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        JSONRESPONSE -- returns json response for ajax
    """    
    data = {
            'delete_id': startup_id
    }
    the_start = get_startup_service(id=startup_id)
    status = f"{the_start.title} را حذف کرد"
    status_of_user(track_info, status, 'delete-startup')
    create_notification(the_start.owner, 'delete-startup', the_start)

    the_start.delete()
    return data


def list_referee_service(track_info, search, offset):
    """list of all users that have to role of referee and searchable by:
       - first_name
       - last_name
       - mobile

    Arguments:
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
        search {DICT} -- a dictionary of entered values as GET method
        offset {GET Method} -- for define page number

    Returns:
        DICT -- returns queryset of User objects
    """    
    status = "لیست داوران را دید"
    status_of_user(track_info, status, 'import-list-referee')

    referees = User.objects.filter(role__name='referee')
    the_ref = referees
    if search.get("fname"):
        referees = referees.filter(first_name__icontains=search.get("fname"))
        the_ref = referees
    if search.get("lname"):
        referees = referees.filter(last_name__icontains=search.get("lname"))
        the_ref = referees
    if search.get("mobile"):
        referees = referees.filter(phone__icontains=search.get("mobile"))
        the_ref = referees
    paginator = Paginator(referees, 30)
    page = offset
    referees = paginator.get_page(page)
    return {'referees': referees,
            'page': page,
            'fname': search.get("fname"),
            'lname': search.get("lname"),
            'the_ref': the_ref,
            'mobile': search.get("mobile")}


def list_investor_service(track_info, search, context, offset):
    """list all users that have the role of investor

    Arguments:
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        TUPLE -- returns tuple of User that have role of investor and a counter (since we are using investors for pagination we need counter)
    """
    investors = User.objects.filter(role__name='investor')
    invest_counter = investors.count()
    status = "لیست سرمایه گذاران را دید"
    status_of_user(track_info, status, 'import-list-investor')
    if search.get("fname"):
        investors = investors.filter(first_name__icontains=search.get("fname"))
        invest_counter = investors.count()
    if search.get("lname"):
        investors = investors.filter(last_name__icontains=search.get("lname"))
        invest_counter = investors.count()
    if search.get("mobile"):
        investors = investors.filter(phone__icontains=search.get("mobile"))
        invest_counter = investors.count()
    paginator = Paginator(investors, 30)
    page = offset
    investors = paginator.get_page(page)
    context.update({
    'investors': investors,
    'fname': search.get("fname"),
    'lname': search.get("lname"),
    'mobile': search.get("mobile"),
    'page': page,
    })
    return investors, invest_counter


def list_investor_activate_service(investors, track_info, can_see):
    """allow user to search throw users with role of investor by:
       - first_name
       - last_name
       - phone

    Arguments:
        search {DICT} -- a dictionary of entered values for search by user
        investors {QUERYSET} -- a queryset of all users with role of investor
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
        can_see {POST Method} -- to define if user can see the startup

    Returns:
        BOOLEAN -- returns True if everythig goes well
    """

    if can_see == 'submit_looks':
        for inv in investors:
            inv.can_see = True
            inv.save()
        status = "تمام سرمایه گذاران میتوانند استارت اپ ها را ببینند"
        status_of_user(track_info, status, 'investors-can-see-startup')

    elif can_see == 'submit_del_looks':
        for inv in investors:
            inv.can_see = False
            inv.save()
        status = "هیچ سرمایه گذارای نمیتواند استارت اپ ها را ببیند"
        status_of_user(track_info, status, 'investors-cant-see-startup')
    return True 


def investor_can_see_service(inv_id, track_info):
    """check if the selected user with field of can_see is True will make it False and vice versa

    Arguments:
        inv_id {INT} -- id of user given by ajax

    Returns:
        BOOLEAN -- returns True if everything goes well
    """    
    data = {
        'add_id': inv_id
    }
    investor = get_user_service(pk=inv_id)
    if investor.can_see == False:
        investor.can_see = True
        investor.save()
    else:
        investor.can_see = False
        investor.save()
    status = f"باعث شد سرمایه گذار {investor} استارت اپ را ببیند"
    status_of_user(track_info, status, 'investor-can-see-startup')
    return data



def list_coach_service(track_info, offset, search):
    """list of all users that have the roles of coach or leader or both
       and searchable by:
       - first_name
       - last_name
       - phone

    Arguments:
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
        offset {GET Method} -- to get pagination
        search {DICT} -- a dictunary of entered values for search

    Returns:
        DICT -- returns dictionary of all coaches and counter and pass search keies fo pagination and placeholder
    """    
    status = "لیست مربیان/داوران را دید"
    status_of_user(track_info, status, 'import-list-coach')
    coaches = User.objects.filter(
        Q(role__name='coach') | Q(role__name='leader')).distinct()
    counter = coaches.count()
    if search.get("fname"):
        coaches = coaches.filter(first_name__icontains=search.get("fname"))
        counter = coaches.count()

    if search.get("lname"):
        coaches = coaches.filter(last_name__icontains=search.get("lname"))
        counter = coaches.count()

    if search.get("mobile"):
        coaches = coaches.filter(phone__icontains=search.get("mobile"))
        counter = coaches.count()

    paginator = Paginator(coaches, 30)
    page = offset
    coaches = paginator.get_page(page)

    return {'coaches': coaches,
            'fname': search.get("fname"),
            'lname': search.get("lname"),
            'mobile': search.get("mobile"),
            'counter': counter}


def list_accelerator_serviece(track_info, offset):
    """list of all accelerators(ShetabDahande)

    Arguments:
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
        offset {GET Method} -- for pagination

    Returns:
        DICT -- returns dictionary of a queryset of accelerators
    """    
    status = "لیست شتاب دهنده ها را دید"
    status_of_user(track_info, status, 'import-list-accelerator')
    accelerators = models.ShetabDahande.objects.prefetch_related('category').select_related('name_namayande').all()
    the_accelerators = accelerators
    paginator = Paginator(accelerators, 30)
    page = offset
    accelerators = paginator.get_page(page)
    return {'accelerators': accelerators,
            'the_accelerators': the_accelerators}


def delete_accelerator_service(track_info, acc_id):
    """get the id of specified accelerator object and deletes it

    Arguments:
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
        acc_id {INT} -- given id from ajax

    Returns:
        DICT -- returns dictionary of data(given id by ajax)
    """    
    data = {
        'delete_id': acc_id
    }
    the_shetab = get_object_or_404(models.ShetabDahande, id=acc_id)
    status = f"شتاب دهنده {the_shetab.name_shtabdahande} را حذف کرد"
    status_of_user(track_info, status, 'delete-accelerator')
    the_shetab.delete()
    return data


def suspend_startup_service(form, startup, track_info):
    """change the selected startup status to suspend or vice versa
       but if the status change to suspend the old status will be saved to return back the status if suspenshion is over

    Arguments:
        form {POST Method} -- to get the value of startup_suspend submit btn
        startup {OBJECT} -- the selected startup
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        BOOLEAN -- returns True if everything goes well
    """
    if 'suspended' == form.get('startup_suspend'):
        startup.old_status = startup.status
        startup.status = 'suspended'
        startup.save()
        status = f"استارتاپ {startup.title} به حالت تعلیغ در آمد"
        status_of_user(track_info, status, 'suspended-startup')
        if form.get('suspend_notification') == "1":
            create_notification(startup.owner, 'suspended-startup', startup)
    elif 'not_suspended' == form.get('startup_suspend'):
        startup.status = startup.old_status
        startup.save()
    return True


def verify_startup_documents_service(form, startup, track_info):
    """if startup documets accept by operational the startup status became accpeted_document
       and store the comment of operational and the status of accepted or failed

    Arguments:
        form {POST Method} -- to get some values to change the status
        startup {OBJECT} -- the selcted startup
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        BOOLEAN -- returns True if everything goes well
    """    
    template = 'email/startup-email.html'
    to = startup.owner.email
    if 'accepted_document' == form['status_document']:
        try:
            th_comments = models.StartupComments.objects.get(
                startup=startup)
            th_comments.doc_stat_status = 'accepted'
            th_comments.doc_stat = form['document_comment']
            th_comments.save()
        except:
            th_comments = models.StartupComments.objects.create(startup=startup,
                                                    doc_stat_status='accepted',
                                                    doc_stat=form['document_comment'])
        finally:
            startup.status = 'accepted_document'
            startup.save()
            status = f"مدارک {startup.title} را تایید کرد"
            status_of_user(track_info, status, 'accept-document')
            if form.get('document_notification') == "1":
                sub, the_message = 'صحت مدارک تیم شما توسط ارزیاب اولیه تایید شد. مراحل بعدی به شما اطلاع رسانی خواهد شد', str(
                    form['document_comment'])
                create_notification(startup.owner, 'accept-document', startup)
                Thread(target=send_email, args=(track_info,), kwargs={
                    "to": [to] , 'template': template, 'sub': sub, 'the_messages': the_message}).start()

    elif 'failed_document' == form['status_document']:

        try:
            th_comments = models.StartupComments.objects.get(
                startup=startup)
            th_comments.doc_stat_status = 'failed'
            th_comments.doc_stat = form['document_comment']
            th_comments.save()
        except:
            th_comments = models.StartupComments.objects.create(startup=startup,
                                                    doc_stat_status='failed',
                                                    doc_stat=form['document_comment'])
        finally:
            startup.status = 'failed_document'
            startup.save()
            status = f"مدارک {startup.title} را رد کرد"
            status_of_user(track_info, status, 'fail-document')
            if form.get('document_notification') == "1":
                sub, the_message = 'صحت مدارک تیم شما توسط ارزیاب اولیه رد شد. لطفا نسبت به تکمیل اطلاعات خود اقدام نمایید', str(
                    th_comments.doc_stat)
                create_notification(startup.owner, 'fail-document', startup)
                Thread(target=send_email, args=(track_info,), kwargs={
                    "to": [to] , 'template': template, 'sub': sub, 'the_messages': the_message}).start()
    return True


def startup_status_service(form, track_info, startup):
    """define the Assessment of selected startup if it's accepted of failed
       an email will be sent to owner of the startup if status_notification is 1

    Arguments:
        form {POST Method} -- get entered values to accept or decline
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
        startup {OBJECT} -- the selected startup

    Returns:
        BOOLEAN -- returns True if everything goes well
    """    
    template = 'email/startup-email.html'
    to = startup.owner.email
    th_comments = models.StartupComments.objects.get(startup=startup)
    if 'accepted' == form['status']:
        th_comments.startup_stat_status = 'accepted'
        th_comments.startup_stat = form['admin_comment']
        th_comments.save()
        startup.status = 'accepted'
        startup.save()
        status = f"وضعیت استارت اپ {startup.title} را قبول کرد"
        status_of_user(track_info, status, 'accept-first')
        if form.get('status_notification') == "1":
            sub = 'وضعیت طرح ارسالی شما در صد استارتاپ : تایید شده توسط ارزیاب اولیه'
            the_message = th_comments.startup_stat
            create_notification(startup.owner, 'accept-first', startup)
            Thread(target=send_email, args=(track_info,), kwargs={
                "to": [to] , 'template': template, 'sub': sub, 'the_messages': the_message}).start()


    elif 'failed' == form['status']:
        th_comments.startup_stat_status = 'failed'
        th_comments.startup_stat = form['admin_comment']
        th_comments.save()
        startup.status = 'failed'
        startup.save()
        status = f"وضعیت استارت اپ {startup.title} را رد کرد"
        status_of_user(track_info, status, 'fail-first')
        if form.get('status_notification') == "1":
            sub, the_message = 'وضعیت طرح ارسالی شما در صد استارتاپ :رد شده توسط ارزیاب اولیه', str(th_comments.startup_stat)
            create_notification(startup.owner, 'fail-first', startup)
            Thread(target=send_email, args=(track_info,), kwargs={
                "to": [to] , 'template': template, 'sub': sub, 'the_messages': the_message}).start()
    return True


def verify_not_presence_referee_service(form, startup, track_info):
    """define not presence referee status of selected startup
       send email and notification to owner of the startup if his/her startup is accpeted for not presence referee

    Arguments:
        form {POST Method} -- to get entered comments and assign it to StartupComments
        startup {OBJECT} -- the selected startup
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        BOOLEAN -- returns True if everything goes well
    """    
    template = 'email/startup-email.html'
    to = startup.owner.email
    th_comments = models.StartupComments.objects.get(startup=startup)
    if 'accepted_not_presence' == form['status_modir']:
        th_comments.no_referee_stat_status = 'accepted'
        th_comments.no_referee_stat = form['modir_comment']
        th_comments.save()
        startup.status = 'accepted_not_presence'
        startup.no_referee_stat = form['modir_comment']
        startup.save()
        status = f"داوری غیر حضوری استارت اپ {startup.title} را قبول کرد"
        status_of_user(track_info, status, 'accept-first_referee')
        if form.get('not_presence_referee_notificaion') == "1":
            sub, the_message = 'تایید داوری غیر حضوری شده توسط مدیر عملیاتی', str(
                th_comments.no_referee_stat)
            create_notification(startup.owner, 'accept-first_referee', startup)
            Thread(target=send_email, args=(track_info,), kwargs={
                "to": [to] , 'template': template, 'sub': sub, 'the_messages': the_message}).start()


    elif 'failed_not_presence' == form['status_modir']:
        th_comments.no_referee_stat_status = 'failed'
        th_comments.no_referee_stat = form['modir_comment']
        th_comments.save()
        startup.status = 'failed_not_presence'
        startup.save()
        status = f"داوری غیر حضوری استارت اپ {startup.title} را رد کرد"
        status_of_user(track_info, status, 'fail-first_referee')
        if form.get('not_presence_referee_notificaion') == "1":
            sub, the_message = 'رد داوری غیر حضوری شده توسط مدیر عملیاتی', str(
                th_comments.no_referee_stat)
            create_notification(startup.owner, 'fail-first_referee', startup)
            Thread(target=send_email, args=(track_info,), kwargs={
                "to": [to] , 'template': template, 'sub': sub, 'the_messages': the_message}).start()
    return True


def verify_presence_referee_service(form, startup, track_info):
    """operational will accept or decline startups presence referee
       and send email and notification to  the owner of satrtup

    Arguments:
        form {POST Method} -- to get comments and entered values for StartupComments
        startup {OBJECT} -- selected startup
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        BOOLEAN -- returns True if everything goes well
    """    
    template = 'email/startup-email.html'
    to = startup.owner.email
    th_comments = models.StartupComments.objects.get(startup=startup)
    if 'accepted_presence' == form['status_presence']:
        startup.status = 'accepted_presence'
        startup.save()
        th_comments.referee_stat_status = 'accepted'
        th_comments.referee_stat = form['presence_comment']
        th_comments.save()
        status = f"داوری حضوری استارت اپ {startup.title} را قبول کرد"
        status_of_user(track_info, status, 'accept-presence')
        if form.get('presence_referee_notification') == "1":
            sub, the_message = ' تایید داوری حضوری شده توسط مدیر عملیاتی', str(
                th_comments.referee_stat)
            create_notification(startup.owner, 'accept-presence', startup)
            Thread(target=send_email, args=(track_info,), kwargs={
                "to": [to] , 'template': template, 'sub': sub, 'the_messages': the_message}).start()


    elif 'failed_presence' == form['status_presence']:
        startup.status = 'failed_presence'
        startup.save()
        th_comments.referee_stat_status = 'failed'
        th_comments.referee_stat = form['presence_comment']
        th_comments.save()
        status = f"داوری حضوری استارت اپ {startup.title} را رد کرد"
        status_of_user(track_info, status, 'fail-presence')
        if form.get('presence_referee_notification') == "1":
            sub, the_message = 'رد داوری حضوری شده توسط مدیر عملیاتی', str(
                th_comments.referee_stat)
            create_notification(startup.owner, 'fail-presence', startup)
            Thread(target=send_email, args=(track_info,), kwargs={
                "to": [to] , 'template': template, 'sub': sub, 'the_messages': the_message}).start()

    return True


def add_to_investor_service(form, startup, track_info):
    """change the status of startup to add_investor or vice versa 
       it's the final stage for startup verification(for now)
       after status changes email and notifiacation will be sent to the owner of startup

    Arguments:
        form {POST Method} -- to check values to change status
        startup {OBJECT} -- selected startup
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        BOOLEAN -- returns True if everything goes well
    """    
    template = 'email/startup-email.html'
    to = startup.owner.email
    if form['investor_panel'] == 'accepted_presence':
        startup.status = 'accepted_presence'
        startup.save()
        if form.get('invest_notification') == "1":
            status = f"وضعیت استارت اپ {startup.title} را به {startup.status} تغییر داد"
            status_of_user(track_info, status, 'available-for-invest')
            create_notification(startup.owner, 'available-for-invest', startup)
            sub, the_message = 'وضعیت استارتاپ شما', 'تیم شما وارد مرحله سرمایه گذاری شد. مراحل بعدی به شما اطلاع رسانی خواهد شد'
            Thread(target=send_email, args=(track_info,), kwargs={
                "to": [to] , 'template': template, 'sub': sub, 'the_messages': the_message}).start()

    elif form['investor_panel'] == 'add_investor':
        startup.status = 'add_investor'
        startup.save()
        if form.get('invest_notification') == "1":
            status = f"وضعیت استارت اپ {startup.title} را به {startup.status} تغییر داد"
            status_of_user(track_info, status, 'not-available-for-invest')
            create_notification(startup.owner, 'not-available-for-invest', startup)
            sub, the_message = 'وضعیت استارتاپ شما', 'تیم شما از مرحله سرمایه گذاری حذف شد. مراحل بعدی به شما اطلاع رسانی خواهد شد'
            Thread(target=send_email, args=(track_info,), kwargs={
                "to": [to] , 'template': template, 'sub': sub, 'the_messages': the_message}).start()

    return True


def reconsider_service(startup_id, comment, track_info):
    """allow operational to reconsider of the status of startup is failed
       and send a new

    Arguments:
        startup_id {INT} -- the id of selected startup
        comment {STRING} -- the comment which operational wrote to reconsider
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        DICT -- returns the comment and the id of startup that have been send by ajax
    """    
    data = {
        'acceptid': startup_id,
        'admin_comment_apply': comment,
    }
    startup = get_startup_service(id=startup_id)
    startup.status = 'accepted'
    startup.save()
    startup.startupcomment.startup_stat = comment
    startup.startupcomment.startup_stat_status = 'accepted'
    startup.startupcomment.save()
    status = f"استارتاپ {startup.title} مورد تجدید نظر قرار گرفت"
    status_of_user(track_info, status, 'reconsider')
    create_notification(startup.owner, 'reconsider', startup)

    return data


def edit_startup_instance_service(id, user, track_info, context):
    """get the instances of selected startup and team members and UserProfile and User
       information that belongs to owner of startup

    Arguments:
        id {INT} -- the id of the startup
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
        context {DICT} -- an empty deictionay of contextes

    Returns:
        TUPLE -- returns tuple of objects and querysets
    """    
    startup = get_startup_service(id=id)
    is_op = get_role_service(name='operational')
    if (startup.owner == user and startup.status == 'failed_document') or user.is_admin or user.user_type == 'manager' or is_op in user.role.all():
        categories = Categories.objects.all()
        userprofile = get_object_or_404(
            models.UserProfile, user__pk=startup.owner.pk)
        startupform1 = StartUpForm1(instance=startup)
        startupform2 = StartUpForm2(instance=startup)
        startupform3 = StartUpForm3(instance=startup)
        startupform6 = StartUpForm6(instance=startup)
        startupform5 = StartUpForm5(instance=startup)
        startupform4 = StartUpForm4(instance=startup)
        userprofile_form = LeaderForm(instance=userprofile)
        leader_form = LeaderUserForm(instance=userprofile.user)
        user_leader = get_user_service(pk=startup.owner.pk)
        team_member = models.TeamMember.objects.filter(startup=startup)
        status = f"مشخصات استارت اپ {startup.title} را تغییر داد"
        status_of_user(track_info, status, 'import-edit-startup')
        context.update({'startupform1': startupform1,
                    'startupform2': startupform2,
                    'startupform3': startupform3,
                    'startupform5': startupform5,
                    'startup_e': startupform6,
                    'startup_p': startupform4,
                    'userprofile_form': userprofile_form,
                    'leader_form': leader_form,
                    'user_leader': user_leader,
                    'startup': startup,
                    'team_member': team_member,
                    "categories": categories})
        return userprofile, startup, team_member
    return 'not_allowed'


def edit_startup_service(startup, user, userprofile, form, file_value, track_info, team_member):
    """get all the forms for startup and owner and team members of startup with instances
       and check the validation of forms

    Arguments:
        startup {OBJECT} -- the selected startup
        userprofile {OBJECT} -- the userprofile of the owner of startup
        form {POST Method} -- to get image and birth date and required money
        file_value {FILES Method} -- to get the resume files for team members

    Returns:
        BOOLEAN -- returns True if forms are valid else returns False
    """ 
    startupform1 = StartUpForm1(
        form, file_value, instance=startup)
    startupform6 = StartUpForm6(
        form, file_value, instance=startup)
    startupform4 = StartUpForm4(
        form, file_value, instance=startup)
    startupform5 = StartUpForm5(form, instance=startup)
    startupform3 = StartUpForm3(form, instance=startup)
    userprofile_form = LeaderForm(form, instance=userprofile)
    leader_form = LeaderUserForm(form, instance=userprofile.user)
    if startupform1.is_valid() and startupform4.is_valid() and startupform5.is_valid() and startupform6.is_valid() and startupform3.is_valid() and userprofile_form.is_valid() and leader_form.is_valid():
        try:
            image_b64 = form.get('avatar_base64')
            th_img , ext = resize_pics(image_b64)
            startupform1.instance.image.save(f'startup.{ext}', files.File(th_img), save=False)

        except:
            pass

        s_lists = get_list(form['start_date'])
        s_date = JalaliDate(
            s_lists[0], s_lists[1], s_lists[2]).to_gregorian()
        startupform3.instance.start_date = s_date

        startupform3.instance.require_money = int(
            ''.join(form.get('require_money').split(',')))

        startupform1.instance.category.clear()
        for cat in form.getlist('category'):
            startupform1.instance.category.add(cat)
        startupform1.instance.site = form.get('site')
        startupform1.save()
        userprofile_form.save()
        startupform3.save()
        startupform4.save()
        startupform5.save()
        startupform6.save()
        l_lists = get_list(form['birth_date'])
        l_date = JalaliDate(
            l_lists[0], l_lists[1], l_lists[2]).to_gregorian()
        leader_form.instance.birth_date = l_date
        leader_form.save()
        t_first_name = (i for i in form.getlist('first_namel[]'))
        t_last_name = (i for i in form.getlist('last_namel[]'))
        t_phone = (i for i in form.getlist('mobilel[]'))
        t_email = (i for i in form.getlist('email_l[]'))
        t_birth_date = (i for i in form.getlist('birthdayl[]'))
        tgrade = (i for i in form.getlist('educationl1[]'))
        t_the_role = (i for i in form.getlist('sidel[]'))
        t_duration_per_month = (i for i in form.getlist('averagel[]'))
        t_saham = (i for i in form.getlist('stockl[]'))
        t_skill = (i for i in form.getlist('expertisel[]'))
        t_role_in_startup = (i for i in form.getlist('role[]'))
        index_of_pdf = (i for i in file_value.getlist('cv[]'))
        index_of_avatar = (i for i in file_value.getlist('t_avatar[]'))
        for i, team in enumerate(team_member):

            lists = get_list(t_birth_date.__next__())
            date = JalaliDate(
            lists[0], lists[1], lists[2]).to_gregorian()
            try:
                team.t_first_name = t_first_name.__next__()
                team.t_last_name = t_last_name.__next__()
                team.t_phone = t_phone.__next__()
                team.t_email = t_email.__next__()
                team.t_birth_date = date
                team.tgrade = tgrade.__next__()
                team.t_the_role = t_the_role.__next__()
                team.t_duration_per_month = t_duration_per_month.__next__()
                team.t_saham = t_saham.__next__()
                team.t_skill = t_skill.__next__()
                team.t_role_in_startup = t_role_in_startup.__next__()
                team.save()
                try:
                    team.t_linkdin=form.getlist('linkdinl[]')[i]
                    team.save()
                except:
                    pass
                if form.getlist('avatar_index')[i] == str(1):
                    team.t_avatar = index_of_avatar.__next__()
                    team.save()

                if form.getlist('cv_index')[i] == str(1):
                    team.t_cv = index_of_pdf.__next__()
                    team.save()
            except Exception as e:
                logger.error(str(e))
        if startupform1.instance.owner == user:
            startupform1.instance.status = 'editing'
            startupform1.save()
        status = f"مشخصات استارت اپ {startup.title} را تغییر داد"
        status_of_user(track_info, status, 'editing-startup')
        create_notification(startup.owner, 'editing-startup', startup)
        return True
    else: return tuple(startupform1, startupform4, startupform5, startupform6, startupform3, userprofile_form, leader_form)


def edit_accelerator_instance_service(pk, context):
    """get instances of selected accelerator object and all categories

    Arguments:
        context {DICT} -- an empety dictionary of context

    Returns:
        TUPLE -- returns tuple of object and queryset and form
    """    
    shetab = models.ShetabDahande.objects.prefetch_related('category').select_related('name_namayande').get(pk=pk)
    categories = Categories.objects.all()
    shetab_form = ShetabDahandeForm(instance=shetab)
    context.update({'shetab_form': shetab_form, 'categories': categories})
    return shetab


def edit_accelerator_service(form, shetab, track_info):
    """update the informaion about an accelerator with Model Form

    Arguments:
        form {POST Method} -- to get image and leader as name_namayande
        shetab {OBJECT} -- the selected accelerator object
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        BOOLEAN -- returns True if form is valid else returns False
    """  
    shetab_form = ShetabDahandeForm(form, instance=shetab)
    if shetab_form.is_valid():
        try:
            image_b64 = form.get('avatar_base64')
            th_img , ext = resize_pics(image_b64)
            shetab_form.instance.image.save(f'accelerator.{ext}', files.File(th_img), save=False)
        except Exception as e:
            logger.error(str(e))

        if form.getlist('name_namayande'):
            for person_id in form.getlist('name_namayande'):
                if not re.search(r'\d', person_id, re.I): continue
                namayande = get_user_service(pk=int(person_id))
                shetab_form.instance.name_namayande = namayande

        shetab_form.instance.category.clear()
        status = f"مشخصات شتاب دهنده {shetab_form.instance.name_shtabdahande} را تغییر داد"
        status_of_user(track_info, status, 'edit-accelerator')
        shetab_form.save()

        for cat in form.getlist('category'):
            shetab_form.instance.category.add(cat)
        return True
    else:
        logger.error(str(shetab_form.errors))
        return shetab_form.errors



def informaion_accelerator_service(pk, track_info):
    """a detailed informaion about an accelerator

    Arguments:
        pk {INT} -- the id of seleclted accelerator object
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        DICT -- returns dictionary of accelerator object
    """    
    accelerator = models.ShetabDahande.objects.prefetch_related('category').select_related('name_namayande').get(pk=pk)
    status = f"شتاب دهنده {accelerator.name_shtabdahande} را دید"
    status_of_user(track_info, status)
    return {'accelerator': accelerator}



def create_accelerator_instances():
    """fetch categories and ShetabDahanderForm

    Returns:
        DICT -- returns dictionary of context (categories, form)
    """    
    shetab_form = ShetabDahandeForm()
    categories = Categories.objects.all()
    return {
        'shetab_form': shetab_form,
        'categories': categories,
    }


def create_accelerator_service(form, track_info):
    """get the ShetabDahande form and checks if the entered values are valide
       the get image(that is based-64) and resize it and then save it
       and get a leader to assign to accelerator as name_namayande
       and assign categories to accelerator

    Arguments:
        form {POST Method} -- to define form method and get entered values
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        BOOLEAN -- returns True if form is valid else returns shetab_form errors
    """    
    shetab_form = ShetabDahandeForm(form)
    if shetab_form.is_valid():
        try:
            image_b64 = form.get('avatar_base64')
            th_img , ext = resize_pics(image_b64)
            shetab_form.instance.image.save(f'accelerator.{ext}', files.File(th_img), save=False)
        except:
            pass
        try:
            shetab_form.instance.user.user_type = 'shetab'
        except:
            pass
        if form.getlist('name_namayande'):
            for person_id in form.getlist('name_namayande'):
                if not re.search(r'\d', person_id, re.I): continue
                namayande = get_user_service(pk=int(person_id))
                shetab_form.instance.name_namayande = namayande

        shetab_form.save()
        status = f"شتاب دهنده {shetab_form.instance.name_shtabdahande} را ساخت"
        status_of_user(track_info, status, 'create-accelerator')

        for cat in form.getlist('category'):
            shetab_form.instance.category.add(cat)
        return True
    else:
        logger.error(str(shetab_form.errors))
        return shetab_form.errors





def add_for_invest_service(startup_id, user, track_info):
    """when the status of the startup become add_to_invest investors can see the startups that have same category with them 
       and accept or decline to invest or try to meet the owner of startup

    Arguments:
        startup_id {INT} -- startup id that came from ajax
        user {OBJECT} -- requested user
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        JSONRESPONSE -- returns data that contains the id of startup
    """    
    data = {
        'startup_id': startup_id,
    }
    startup = get_startup_service(id=startup_id)
    try:
        te_investor = models.Investors.objects.get(
            user=user, startup=startup)
        if te_investor.status == 0:
            te_investor.status = 1
            te_investor.save()
            status = f"می خواهد در جلسه با استارت اپ {te_investor.startup} شرکت کند"
            status_of_user(track_info, status, 'accept-session-investor')
            create_notification(startup.owner, 'accept-session-investor', user)
        elif te_investor.status == 1:
            te_investor.status = 0
            te_investor.save()
            status = f"نمی خواهد در جلسه با استارت اپ {te_investor.startup} شرکت کند"
            status_of_user(track_info, status, 'fail-session-investor')
            create_notification(startup.owner, 'fail-session-investor', user)

    except:
        te_investor = models.Investors.objects.create(
            user=user, startup=startup, status=1)
        status = f"می خواهد در جلسه با استارت اپ {te_investor.startup} شرکت کند"
        status_of_user(track_info, status, 'accept-session-investor')
        create_notification(startup.owner, 'accept-session-investor', user)

    return data


def informaion_instance_service(pk, user, context, track_info):
    """get the instances of startup and StartupComments and selected leader/presence referees/not presence referees

    Arguments:
        pk {PRIMARY KEY} -- the unique value to get selected startup
        user {OBJECT} -- requested user
        context {DICT} -- a dictionary to update with instances
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        TUPLE -- reutrns tuple of querysets of referees and startup object
    """    
    startup = models.StartUp.objects.prefetch_related('category','requests').select_related('rahbar_asli', 'shetab_dahande', 'rahbar').get(pk=pk)
    status = f"اطلاعات استارت اپ {startup.title} را دید"
    status_of_user(track_info, status, 'import-information')
    
    refers = models.Referee.objects.filter(
        startup=startup, scored=True, the_type='pres')
    score_refers = models.Referee.objects.select_related('user').filter(
        startup=startup, the_type='pres')
    not_refers = models.Referee.objects.filter(
        startup=startup, scored=True, the_type='not_pres')
    score_not_refers = models.Referee.objects.select_related('user').filter(
        startup=startup, the_type='not_pres')
    th_leaders = LeaderModel.objects.filter(startup=startup, status=1)
    is_operational = get_role_service(name='operational')

    try:

        is_not_pres_referee = models.Referee.objects.get(
            user=user, startup=startup, the_type='not_pres')
    except:
        is_not_pres_referee = None

    try:

        is_pres_referee = models.Referee.objects.get(
            user=user, startup=startup, the_type='pres')

    except:
        is_pres_referee = None

    referee_form = RefereeForm()
    try:
        the_total_score = sum(ref.total_score for ref in refers)/refers.count()
    except:
        the_total_score = 0

    try:
        the_total_score2 = sum(
            ref.total_score for ref in not_refers)/not_refers.count()
    except:
        the_total_score2 = 0

    context.update({'startup': startup,
        'referee_form': referee_form,
        'is_referee': is_not_pres_referee,
        'is_not_referee': is_pres_referee,
        'refers': refers,
        'score_refers': score_refers,
        'score_not_refers': score_not_refers,
        'not_refers': not_refers,
        'the_total_score': the_total_score,
        'the_total_score2': the_total_score2,
        'th_leaders': th_leaders,})
    return is_pres_referee, is_not_pres_referee, startup, is_operational
    

def information_pres_referee_score_service(user, form, is_pres_referee, startup, track_info, is_operational):
    """the presence referee can score startup here. the scores will be stored to database as dict
       the values and name tag will be pickled.
       that is because to lesser the occupation of database and this scores has no use in other pages

    Arguments:
        user {OBJECT} -- requested user
        form {POST Method} -- to get entered values
        is_pres_referee {OBJECT} -- to use requested user(presence referee) as instance for RefereeForm
        startup {OBJECT} -- selected startup
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        STRING -- returns pres_referee_score_success if everything goes well else returns error
    """    
    try:
        th_nomre = {
            'score_product1': form['score_product1'],
            'score_product2': form['score_product2'],
            'score_product3': form['score_product3'],
            'score_team1': form['score_team1'],
            'score_team2': form['score_team2'],
            'score_team3': form['score_team3'],
            'score_team4': form['score_team4'],
            'score_team5': form['score_team5'],
            'score_team6': form['score_team6'],
            'score_team7': form['score_team7'],
            'score_team8': form['score_team8'],
            'score_business1': form['score_business1'],
            'score_business2': form['score_business2'],
            'score_business3': form['score_business3'],
            'score_business4': form['score_business4'],
            'score_business5': form['score_business5'],
            'score_business6': form['score_business6'],
            'score_business7': form['score_business7'],
            'score_business8': form['score_business8'],
            'score_investment1': form['score_investment1'],
            'score_investment2': form['score_investment2'],
            'score_investment3': form['score_investment3'],
            'score_investment4': form['score_investment4'],
            'score_investment5': form['score_investment5'],
            'score_investment6': form['score_investment6'],
            'score_investment7': form['score_investment7'],
        }

        if is_operational in user.role.all() or user.is_admin or user.user_type == 'manager':
            is_pres_referee = models.Referee.objects.get(pk=int(form.get('score_for_referee')))
            user = is_pres_referee.user

        th_db_nomre = pickle.dumps(th_nomre)
        referee_form_pres = RefereeForm(
            form, instance=is_pres_referee)
        if referee_form_pres.is_valid():
            referee_form_pres.instance.nomre = th_db_nomre
            referee_form_pres.instance.startup = startup
            referee_form_pres.instance.user = user
            if form.get('wants_to_lead_pres_ref') == '1':
                referee_form_pres.instance.lead = True
                status = f"داور {referee_form_pres.instance.user.first_name} {referee_form_pres.instance.user.last_name} علاقه به راهبری استارت آپ {statrup.title} را دارد"
                status_of_user(track_info, status, 'referee-wants-to-lead')
            if form.get('wants_to_invest_pres_ref') == '1':
                referee_form_pres.instance.invest = True
                status = f"داور {referee_form_pres.instance.user.first_name} {referee_form_pres.instance.user.last_name} علاقه به سرمایه گذاری استارت آپ {statrup.title} را دارد"
                status_of_user(track_info, status, 'referee-wants-to-invest')
            if form.get('example') == '0':
                referee_form_pres.instance.is_accepted = True
                status = f"{referee_form_pres.instance.startup.title} استارت اپ را تایید کرد"
                status_of_user(track_info, status, 'accept-referee-scores-pres')
                create_notification(startup.owner, 'accept-referee-scores-pres', user)

            elif form.get('example') == '1':
                referee_form_pres.instance.is_accepted = False
                status = f"{referee_form_pres.instance.startup.title} استارت اپ را رد کرد"
                status_of_user(track_info, status, 'fail-referee-scores-pres')
                create_notification(startup.owner, 'fail-referee-scores-pres', user)

            referee_form_pres.instance.scored = True

            vote1_ref = ((int(form['score_product1']) + int(
                form['score_product2']) + int(form['score_product3']))/3*35)/100
            vote2_ref = ((int(form['score_team1']) + int(form['score_team2']) + int(form['score_team3']) + int(form['score_team4']) + int(
                form['score_team5']) + int(form['score_team6']) + int(form['score_team7']) + int(form['score_team8']))/8*20)/100
            vote3_ref = ((int(form['score_business1']) + int(form['score_business2']) + int(form['score_business3']) + int(form['score_business4']) + int(
                form['score_business5']) + int(form['score_business6']) + int(form['score_business7']) + int(form['score_business8']))/8*20)/100
            vote4_ref = ((int(form['score_investment1']) + int(form['score_investment2']) + int(form['score_investment3']) + int(
                form['score_investment4']) + int(form['score_investment5']) + int(form['score_investment6']) + int(form['score_investment7']))/7*20)/100
            total_score = vote1_ref + vote2_ref + vote3_ref + vote4_ref
            referee_form_pres.instance.total_score = total_score
            referee_form_pres.save()
            status = f"به استارت اپ {referee_form_pres.instance.startup.title} نمره داد"
            status_of_user(track_info, status, 'submit-scores')
            create_notification(startup.owner, 'submit-scores', user)
            return 'pres_referee_score_success'
        else:
            logger.error(str(referee_form_pres.errors))
            return referee_form_pres.errors
    except Exception as e:
        logger.error(str(e))
        print(str(e))

    
def informaion_not_pres_referee_score_service(user, form, is_not_pres_referee, startup, track_info, is_operational):
    """the not presence referee can score startup here. the scores will be stored to database as dict
       the values and name tag will be pickled.
       that is because to lesser the occupation of database and this scores has no use in other pages

    Arguments:
        user {OBJECT} -- requested user
        form {POST Method} -- to get entered values
        is_not_pres_referee {OBJECT} -- [description]
        startup {OBJECT} -- selected startup
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        STRING -- returns not_pres_referee_score_success if everything goes well else returns error
    """
    try:
        nomre = {
            'score_full': form['score_full'],
            'score_coordination': form['score_coordination'],
            'score_ability': form['score_ability'],
            'score_market': form['score_market'],
            'score_growth': form['score_growth'],
            'score_competition': form['score_competition'],
            'score_targetmarket': form['score_targetmarket'],
            'score_suggestedvalue': form['score_suggestedvalue'],
            'score_mvp': form['score_mvp'],
            'score_transparency': form['score_transparency'],
            'score_advantage': form['score_advantage'],
            'score_strategy': form['score_strategy'],
            'score_precise': form['score_precise'],
        }
        try:
            if is_operational in user.role.all() or user.is_admin or user.user_type == 'manager':
                is_not_pres_referee = models.Referee.objects.get(pk=int(form.get('score_for_not_referee')))
                user = is_not_pres_referee.user
        except Exception as e:
            print(str(e))
        db_nomre = pickle.dumps(nomre)
        referee_form = RefereeForm(form, instance=is_not_pres_referee)
        if referee_form.is_valid():
            referee_form.instance.startup = startup
            referee_form.instance.user = user
            referee_form.instance.nomre = db_nomre
            if form.get('wants_to_lead_not_pres_ref') == '1':
                referee_form.instance.lead = True
                status = f"داور {referee_form.instance.user.first_name} {referee_form.instance.user.last_name} علاقه به راهبری استارت آپ {statrup.title} را دارد"
                status_of_user(track_info, status, 'referee-wants-to-lead')

            if form.get('wants_to_invest_not_pres_ref') == '1':
                referee_form.instance.invest = True
                status = f"داور {referee_form.instance.user.first_name} {referee_form.instance.user.last_name} علاقه به سرمایه گذاری استارت آپ {statrup.title} را دارد"
                status_of_user(track_info, status, 'referee-wants-to-invest')

            if form.get('score_accept_status'):
                referee_form.instance.is_accepted = True
                status = f"{referee_form.instance.startup.title} استارت اپ را تایید کرد"
                status_of_user(track_info, status, 'accept-referee-scores')
                create_notification(startup.owner, 'accept-referee-scores', user)

            elif form.get('score_feiled_status'):
                referee_form.instance.is_accepted = False
                status = f"{referee_form.instance.startup.title} استارت اپ را رد کرد"
                status_of_user(track_info, status, 'fail-referee-scores')
                create_notification(startup.owner, 'fail-referee-scores', user)

            referee_form.instance.scored = True
            vote1_ref = (
                (int(form['score_full']) + int(form['score_coordination']) + int(form['score_ability']))/3*35)/100
            vote2_ref = ((int(form['score_market']) + int(
                form['score_growth']) + int(form['score_competition']))/3*20)/100
            vote3_ref = ((int(form['score_targetmarket']) + int(form['score_suggestedvalue']) + int(form['score_mvp']) + int(
                form['score_transparency']) + int(form['score_advantage']) + int(form['score_strategy']))/6*35)/100
            vote4_ref = ((int(form['score_precise']))/1*10)/100
            total_score = vote1_ref + vote2_ref + vote3_ref + vote4_ref
            referee_form.instance.total_score = total_score
            referee_form.save()
            status = f"به استارت اپ {referee_form.instance.startup.title} نمره داد"
            status_of_user(track_info, status, 'submit-scores')
            create_notification(startup.owner, 'submit-scores', user)
            return 'not_pres_referee_score_success'
        else:
            logger.error(str(referee_form.errors))
            return referee_form.errors

    except Exception as e:
        logger.error(str(e))


def informaion_select_leader_service(form, startup, track_info):
    """the operational will select a leader(rahbar_asli) for startup here if startup didn't chose accelerator at registration process
       cause the name_namayande of accelerator(ShetabDahande) will become the leader(rahbar_asli) of startup
       but other wise the other leaders that startup chose at registeration process or if the owner didn't choose
       any leader or the leaders that been recommended to startup(OffetToLeader) (if the leaders accpeted to lead)
       will be shown here as recommended leaders but still operational can choose another leader for startup

    Arguments:
        form {POST Method} -- to get enterd valuse(the id of user fo leading)
        startup {OBJECT} -- the selected startup
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        BOOLEAN -- returns True if everything goes well
    """    
    if form.get('companion'):
        rahbar = get_user_service(pk=form.get('companion'))
        startup.rahbar_asli = rahbar

        if startup.is_leader == False:
            startup.status = 'select_leader'
            startup.is_leader = True
        startup.save()

        status = f"{rahbar} را بعنوان راهبر اصلی برای استارت اپ {startup.title} انتخاب کرد"
        status_of_user(track_info, status, 'select-leader')
        if form.get('companion_notification') == "1":
            create_notification(rahbar, 'select-leader', startup)
            create_notification(startup.owner, 'select-leader', rahbar)
        return True

    elif form.get('companionra'):
        shetab = models.ShetabDahande.objects.get(
            pk=form.get('companionra'))
        startup.shetab_dahande = shetab
        startup.save()
        status = f"{shetab} را بعنوان شتاب دهنده برای استارت اپ {startup.title} انتخاب کرد"
        status_of_user(track_info, status, 'selected-as-accelerator')
        if form.get('companionra_notification') == "1":
            create_notification(startup.owner, 'selected-as-accelerator', shetab.name_namayande.first())
            create_notification(shetab.name_namayande.first(), 'selected-as-accelerator', startup)
        return True


def informaion_select_not_pres_referee_service(form, startup, track_info):
    """in this step operational can select/update referees as not presence once for startup

    Arguments:
        form {POST Method} -- to get entered values(id of user with role of referee)
        startup {OBJECT} -- the selected startup
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        BOOLEAN -- returns True if everything goes well
    """    
    if form.getlist('referee'):
        for i, referee_id in enumerate(form.getlist('referee')):
            if not referee_id: continue
            referee = get_user_service(pk=referee_id)
            try:
                npr = models.Referee.objects.get(pk=form.getlist('not_referee_pk')[i])
                npr.user = referee
                npr.save()
            except:
                models.Referee.objects.create(
                    startup=startup,
                    user=referee,
                    the_type='not_pres',
                )
                if form.get('referee_notification') == "1":
                    create_notification(referee, 'select-not-presence-referees', startup)
                    create_notification(startup.owner, 'select-not-presence-referees', referee)
            finally:
                if startup.is_not_presence_referee == False:
                    startup.status = 'select_not_presence_referees'
                    startup.is_not_presence_referee = True
                    startup.save()
                status = f"داور غیر حضوری {referee.first_name} {referee.last_name} استارت اپ {startup.title} را انتخاب کرد"
                status_of_user(track_info, status, 'select-not-presence-referees')
        return True


def informaion_select_pres_referee_service(form, startup, track_info):
    """in this step operational can select/update referees as presence once for startup

    Arguments:
        form {POST Method} -- to get entered values(id of user with role of referee)
        startup {OBJECT} -- the selected startup
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        BOOLEAN -- returns True if everything goes well
    """  
    if form.getlist('presence_referee'):
        for i, referee_id in enumerate(form.getlist('presence_referee')):
            if not referee_id: continue
            referee = get_user_service(pk=int(referee_id))
            try:
                npr = models.Referee.objects.get(pk=form.getlist('referee_pk')[i])
                npr.user = referee
                npr.save()
            except:
                models.Referee.objects.create(
                    startup=startup,
                    user=referee,
                    the_type='pres',
                )
                if form.get('pres_referee_notification') == "1":
                    create_notification(referee, 'select-presence-referees', startup)
                    create_notification(startup.owner, 'select-presence-referees', referee)
            finally:
                if startup.is_presence_referee == False:
                    startup.status = 'select_presence_referee'
                    startup.is_presence_referee = True
                    startup.save()
                status = f"داور  حضوری {referee.first_name} {referee.last_name} استارت اپ {startup.title} را انتخاب کرد"
                status_of_user(track_info, status, 'select-presence-referees')
        return True


def information_request_money_service(form, startup, track_info, user):
    """in this step operational will assign request money for startup

    Arguments:
        form {POST Method} -- to get enterd values ( request money )
        startup {OBJECT} -- selected startup
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
        user {OBJECT} -- requested user

    Returns:
        BOOLEAN -- returns True if everything goes well
    """    
    if form.get('request_money'):
        all_credits = []
        for investor in form.getlist('investor_name'):
            if not investor: continue
            assigned_credit = models.CreditAssigned.objects.get_or_create(
                                                startup=startup,
                                                date=datetime.fromtimestamp(float(form.getlist(f'date-{investor}'))/1000),
                                                credit=int(form.getlist(f'request_money-{investor}')),
                                                )
            try:
                user_ids = investor.split('-')
                for user_id in user_ids:
                    assigned_credit.user.add(get_user_service(pk=int(user_id)))
            except:
                assigned_credit.user.add(get_user_service(pk=int(investor)))
            finally:
                assigned_credit.save()
            all_credits.append(assigned_credit.credit)
        startup.credit = sum(int(cred) for cred in all_credits)
        startup.save()
        
        status = f"{user.first_name} {user.last_name} مبلغ {form.get('request_money')} را برای استارت آپ {startup.title} در خواست کرد"
        status_of_user(track_info, status, 'requested-money-op')
        if form.get('requested_money_notification') == "1":
            create_notification(startup.owner, 'requested-money-op', startup)

        return True


def popup_request_service(pk):
    """get the selected Requests object

    Arguments:
        pk {PRIMARY KEY} -- a unique field to get specific object of Requests table

    Returns:
        OBJECT -- retuns selected Requests object
    """    
    return models.Requests.objects.get(pk=pk)


def manage_request_instance_service():
    """get all the requests money

    Returns:
        QUERYSET -- returns queryset of Requests objects
    """    
    return {"the_requests": models.Requests.objects.select_related('startup').all()}


def manage_request_service(form, track_info):
    """will get Requests id from popup and assign leader comment and if accepted or not by he/she
       and assgin finance comment and if accepted or not

    Arguments:
        form {POST Method} -- to get entered values and track user
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        BOOLEAN -- returns True if everything goes well
    """    
    the_req = popup_request_service(form['id'])
    try:
        if form.get('leader_comment'):
            the_req.leader_comment = form['leader_comment']
            if form.get('status_leader') == 'accept':
                the_req.leader_agree = True
                the_req.status = 'accepted_leader'
                status = f"راهبر درخواست استارت اپ {the_req.startup.title }را قبول کرد"
                status_of_user(track_info, status, 'accept-leader-request')
                create_notification(the_req.startup.owner, 'accept-leader-request', the_req.startup)

            elif form.get('status_leader') == 'failed':
                the_req.leader_agree = False
                the_req.status = 'failed_leader'
                status = f"راهبر درخواست استارت اپ {the_req.startup.title }را رد کرد"
                status_of_user(track_info, status, 'fail-leader-request')
                create_notification(the_req.startup.owner, 'fail-leader-request', the_req.startup)

            the_req.save()
            return True
    except Exception as e:
        logger.error(str(e))
    try:
        if form.get('financial_comment'):
            the_req.investor_comment = form['financial_comment']
            if form.get('status_manage') == 'accept':
                the_req.investor_agree = True
                the_req.status = 'accepted_investor'
                status = f"مالی درخواست استارت اپ {the_req.startup.title }را قبول کرد"
                status_of_user(track_info, status, 'accept-manage-request')
                create_notification(the_req.startup.owner, 'accept-manage-request', the_req.startup)

            elif form.get('status_manage') == 'failed':
                the_req.investor_agree = False
                the_req.status = 'failed_investor'
                status = f"مالی درخواست استارت اپ {the_req.startup.title }را قبول کرد"
                status_of_user(track_info, status, 'fail-manage-request')
                create_notification(the_req.startup.owner, 'fail-manage-request', the_req.startup)

            the_req.save()
            return True
    except Exception as e:
        logger.error(str(e))

    
def request_manage_service(user, track_info):
    """all the requests will be shown if requested user is admin or manager or operational
       but if requsted user is the owner of startup the requests of that specific startup will be shown

    Arguments:
        user {OBJECT} -- requested user
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        DICT -- returns dictionary that contains all requests and the requsts blongs to requested user
    """ 
    all_req = models.Requests.objects.select_related('startup').all().order_by('-created_date')
    the_requests = models.Requests.objects.filter(user=user).order_by('-created_date')
    status = f"وارد صفحه درخواست ها شد"
    status_of_user(track_info, status, 'import-request-money')
    return {"all_req": all_req, "the_requests": the_requests}


def send_request_money_service(form, user, track_info):
    """send new request for money by startup

    Arguments:
        form {POST Method} -- to define data of RequestForm
        user {OBJECT} -- requested user
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        BOOLEAN -- returns True if form is valid
    """    
    request_form = RequestsForm(form)
    if request_form.is_valid():
        request_form.instance.user = user
        request_form.instance.startup = user.startup
        request_form.instance.status = 'waiting'
        request_form.save()
        status = f"درخواست {request_form.instance.request_title} را ثبت کرد"
        status_of_user(track_info, status, 'sending-request-money')
        create_notification(user.startup.rahbar_asli, 'sending-request-money', user.startup)
        return True

    else:
        logger.error(str(request_form.errors))



def remove_referee_from_startup_service(form, track_info):
    """get the id of startup and referee id to remove referee from startup

    Arguments:
        form {POST Method} -- to get refree id and startup id
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        JSONRESPONSE -- returns data that contains the id of startup and id of referee
    """    
    referee_id = form.get('ref_id')
    startup_id = form.get('start_id')
    data = {
        'ref_id': referee_id,
        'start_id': startup_id,
    }
    startup = get_startup_service(pk=int(startup_id))
    referee = models.Referee.objects.get(pk=int(referee_id))
    if referee.the_type == 'pres':
        status = f"داور {referee.user.first_name} {referee.user.last_name} از داوری حضوری استارت آپ {startup.title} حذف شد"
        status_of_user(track_info, status, 'delete-pres-referee')
    else:
        status = f"داور {referee.user.first_name} {referee.user.last_name} از داوری غیر حضوری استارت آپ {startup.title} حذف شد"
        status_of_user(track_info, status, 'delete-not-pres-referee')
    referee.delete()
    return data


def can_score_again_service(form, track_info):
    """after a referee user score an startup the scored Field become True after that referee cannot score again
       if operational press the refresh button the referee scored become False and the referee can score again

    Arguments:
        form {POST Method} -- to get refree id and startup id
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        JSONRESPONSE -- returns data that contains the id of startup and id of referee
    """    
    referee_id = form.get('ref_id')
    startup_id = form.get('start_id')
    data = {
        'ref_id': referee_id,
        'start_id': startup_id,
    }
    referee = models.Referee.objects.get(pk=int(referee_id))
    startup = get_startup_service(pk=int(startup_id))
    referee.scored == False
    referee.save()
    status = f"داور {referee.user.first_name} {referee.user.last_name } می تواند نمرات داده شده به استارت آپ {startup.title} را اصلاح کند"
    status_of_user(track_info, status, 'sending-request-money')
    create_notification(referee.user, 'sending-request-money', startup)
    return data