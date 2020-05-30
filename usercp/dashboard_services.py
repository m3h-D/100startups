from .forms import *
from startups.utils import *
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.db.models import Q
from message.models import SendMessage
from startup.models import Requests
from theevent.models import TheEvent
from usertracker.models import UserTracker, TheStatus
from . import models
from django.shortcuts import get_object_or_404
from threading import Thread
from category.models import Categories
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import files
from django.utils import timezone
from persiantools.jdatetime import JalaliDate, JalaliDateTime
from startups.engine import sms
from random import randint
from django.contrib.auth import authenticate
from startups.object import get_role_service, get_user_service
import logging

logger = logging.getLogger(__name__)




def forget_password_service(track_info, form, protocol, current_site):
    """[get input values(username or email) to send hash code to user email]
    
    Arguments:
        request {[HTTPRequest]} -- [request to check the user]
        form {[GET]} -- [form to check the user is exists with this info]
    """
    user = models.User.objects.filter(Q(username=form['mobile']) | Q(
        email=form['mobile'])).distinct().first()
    if user:
        template = 'email/forget-pass-email.html'
        sub = 'فراموشی رمز عبور'
        the_message = urlsafe_base64_encode(force_bytes(user.pk))
        the_message2 = account_activation_token.make_token(user)
        Thread(target=send_email, args=(track_info,), kwargs={"protocol": protocol, "current_site": current_site,
            "to": [user.email] , 'template': template, 'sub': sub, 'the_messages': the_message, 'the_messages2': the_message2}).start()
        status = f"رمز خود را فراموش کرده"
        status_of_user(track_info, status, 'forget-password')
        success = True
    else:
        success = False
    return success



def new_password_service(form, user):
    """set the password for the requested user
    
    Returns:
        BOOLEAN -- redirect user to login page if success is True
    """
    success = False
    if form.get('new_password'):
        user.set_password(form.get('new_password'))
        user.save()
        success = True
        
    return success


def change_password_service(form, track_info):
    """if the passowrd is valid it will save the new password
    
    Arguments:
        form {FORM Class} -- get the form and set the method and instance of ModelForm
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
    
    Returns:
        BOOLEAN -- returns True if form is valid
    """
    if form.is_valid():
        form.save()
        status = f"رمز خود را تغییر داد"
        status_of_user(track_info, status, 'import-change_pass')
        return True
    else: return False


def change_username_service(form, track_info, user):
    """if the username is not taken it will save the mentioned username for requested user
    
    Arguments:
        form {GET method} -- get the mentioned username from requested user
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
        user {OBJECT} -- requested user
    
    Returns:
        BOOLEAN -- returns True if the username successfully changed eles reutrns False
    """
    try:
        get_user_service(username=form['user_name'])
        # models.User.objects.get(username=form['user_name'])
        return False
    except:
        user.username = form['user_name']
        user.save()
        status = f"نام کاربری خود را تغییر داد"
        status_of_user(track_info, status, 'chenge-username')
        return True


def create_user_get_service(track_info):
    """show the all roles and categories to assign for user
    
    Arguments:
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
    
    Returns:
        TUPLE -- roles and categories in create_user html
    """
    roles = models.Role.objects.all()
    categories = Categories.objects.all()
    user_form = KarmandForm()
    try:
        status = f"وارد صفحه ساخت کاربر شد"
        status_of_user(track_info, status, 'import-create-user')
    except:
        pass
    return user_form, roles, categories


def create_user_post_service(user_form, form, track_info):
    """create a user if there is no errors else returns the extra_tags of erros for messges module
    
    Arguments:
        user_form {FORM Class} -- a ModelForm of User table
        form {POST} -- a list of values to assign categories and roles for user
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
    
    Returns:
        STRING -- returns True if user successfully created else returns the extra_tags errors
    """
    user_form = KarmandForm(form)
    if user_form.is_valid():
        user_form.save()
        for cat in form.getlist('category'):
            user_form.instance.category.add(cat)
        for role in form.getlist('role'):
            user_form.instance.role.add(role)

        user_form.instance.user_type = 'karmand'
        user_form.instance.set_password(form['password'])
        user_form.save()
        try:
            status = f"کاربر {user_form.instance.first_name} {user_form.instance.last_name} را ساخت"
            status_of_user(track_info, status, 'creating-user')
            
        except:
            pass
        return True
    elif models.User.objects.filter(phone=form.get('phone')):
        logger.error(user_form.errors)
        return 'phone_exist'
    elif models.User.objects.filter(username=form.get('username')):
        logger.error(user_form.errors)
        return 'username_exist'
    elif models.User.objects.filter(email=form.get('email')):
        logger.error(user_form.errors)
        return 'email_exist'
    else:
        logger.error(user_form.errors)
        return 'smtww'



def list_user_service(search, track_info):
    """searchable list of users
    
    Arguments:
        search {DICT} -- a dictionary of input boxes name and page number
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
    
    Returns:
        DICT -- returns dictionary of contexts
    """
    try:
        status = "لیست کاربران را دید"
        status_of_user(track_info, status, 'import-list-user')
    except:
        pass
    th_roles = models.Role.objects.all()
    th_manager = get_user_service(user_type='manager')
    # th_manager = models.User.objects.get(user_type='manager')
    Users = models.User.objects.filter(
        is_admin=False).exclude(pk=th_manager.pk).order_by('-pk')
    the_users = Users
    if search.get('role_input'):
        try:
            db_role = get_role_service(name=search.get('role_input'))
        except models.Role.DoesNotExist:
            db_role = None
        if search.get('role_input') == 'startup':
            Users = models.User.objects.filter(user_type='startup')
            the_users = Users
            try:
                status = f"کاربر {Users.first().first_name} {Users.first().last_name} را جستجو کرد"
                status_of_user(track_info, status, 'search-list-user')
            except:
                pass

        else:
            Users = Users.filter(role=db_role)
            the_users = Users
            try:
                status = f"کاربر {Users.first().first_name} {Users.first().last_name} را جستجو کرد"
                status_of_user(track_info, status, 'search-list-user')
            except:
                pass
    if search.get('fname'):
        Users = Users.filter(first_name__icontains=search.get('fname'))
        the_users = Users
        try:
            status = f"کاربر {Users.first().first_name} {Users.first().last_name} را جستجو کرد"
            status_of_user(track_info, status, 'search-list-user')
        except:
            pass
    if search.get('lname'):
        Users = Users.filter(last_name__icontains=search.get('lname'))
        the_users = Users
        try:
            status = f"کاربر {Users.first().first_name} {Users.first().last_name} را جستجو کرد"
            status_of_user(track_info, status, 'search-list-user')
        except:
            pass
    if search.get('email'):
        Users = Users.filter(email__icontains=search.get('email'))
        the_users = Users
        try:

            status = f"کاربر {Users.first().first_name} {Users.first().last_name} را جستجو کرد"
            status_of_user(track_info, status, 'search-list-user')
        except:
            pass


    if search.get('the_phone'):
        Users = Users.filter(phone__icontains=search.get('the_phone'))
        the_users = Users
        try:

            status = f"کاربر {Users.first().first_name} {Users.first().last_name} را جستجو کرد"
            status_of_user(track_info, status, 'search-list-user')
        except:
            pass
    paginator = Paginator(Users, 30)
    page = search.get('offset')

    try:
        Users = paginator.page(page)
    except PageNotAnInteger:
        Users = paginator.page(1)
    except EmptyPage:
        Users = paginator.page(paginator.num_pages)
    return {
        'Users': Users,
        'fname': search.get('fname'),
        'lname': search.get('lname'),
        'email': search.get('email'),
        'role_input': search.get('role_input'),
        'the_users': the_users,
        'th_roles': th_roles,
        'the_phone': search.get('the_phone'),
    }




def delete_user_service(user_id, track_info):
    """get user_id from ajax and delete the user
    
    Arguments:
        user_id {STRING} -- get the str of user id and do a queryset in User model
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
    
    Returns:
        DICT -- returns dictionary that contains user_id
    """
    data = {
            'delete_id': user_id
        }
    the_user = get_user_service(id=int(user_id))
    # the_user = models.User.objects.get(id=int(user_id))
    the_user.delete()
    status = f"کاربر {the_user.first_name} {the_user.first_name} {the_user.phone} را حذف کرد"
    status_of_user(track_info, status, 'delete-user')
    return data


def edit_user_get_service(track_info, pk):
    """get Karmand form for selected user 
    
    Arguments:
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
    
    Returns:
        TUPLE -- returns an instance of Karmand form for selected user
    """
    user = get_user_service(pk=pk)
    user_form = KarmandForm(instance=user)
    roles = models.Role.objects.all()
    categories = Categories.objects.all()
    status = f"مشخصات {user_form.instance.first_name} {user_form.instance.last_name} را تغییر داد"
    status_of_user(track_info, status, 'import-edit-user')
    return user, user_form, roles, categories


def edit_user_post_service(form, file_value, track_info, user):
    """the post method of edit user part will get values and files modify user informations
    
    Arguments:
        form {POST method} -- get the request.POST 
        file_value {FILES method} -- get the request.FILES
    
    Returns:
        BOOLEAN/ERRORS -- returns True if user edited successfully else returns form errors
    """
    try:
        user_form = KarmandForm(form, file_value, instance=user)
        if user_form.is_valid():
            try:
                image_b64 = form.get('avatar_base64')
                th_img , ext = resize_pics(image_b64)
                user_form.instance.avatar.save(f'user.{ext}', files.File(th_img), save=False)
            except Exception as e:
                print(str(e))
            user_form.instance.category.clear()
            user_form.instance.role.clear()
            try:
                user_form.instance.set_password(form["password"])
            except:
                pass
            user_form.save()
            for cat in form.getlist('category'):
                user_form.instance.category.add(cat)
            for role in form.getlist('role'):
                user_form.instance.role.add(role)
                if user_form.instance.user_type == 'startup':
                    user_form.instance.user_type2 = 'karmand'
                else:
                    user_form.instance.user_type = 'karmand'
            user_form.save()
            status = f"مشخصات {user_form.instance.first_name} {user_form.instance.last_name} را تغییر داد"
            status_of_user(track_info, status, 'editing-user')
        return True
    except Exception as e:
        return str(e)


def add_to_mentor_service(track_info, acc_id):
    """get the user id from ajax request and add user as mentor user if the user mentor status is false
    
    Arguments:
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
        acc_id {INT} -- the id of user
    
    Returns:
        DICT -- returns back the user id
    """
    data = {
        'add_id': acc_id,
    }
    person = get_user_service(id=acc_id)
    # person = get_object_or_404(models.User, id=acc_id)
    if person.add_to_mentors == False:
        person.add_to_mentors = True
        person.save()
        try:
            status = f"{person.first_name} {person.last_name} را به صفحه منتور ها اضافه کرد"
            status_of_user(track_info, status, 'add-user-mentors')
        except:
            pass

    else:
        person.add_to_mentors = False
        person.save()
        status = f"{person.first_name} {person.last_name} را از صفحه منتور ها حذف کرد"
        try:
            status = f"{person.first_name} {person.last_name} را به صفحه منتور ها اضافه کرد"
            status_of_user(track_info, status, 'delete-user-mentors')
        except:
            pass
    return data



# def profile_service():



def dashboard_roles_service(receiver, context):
    """all the roles to do some condition base of user role
    
    Arguments:
        receiver {REQUEST} -- requested user
    
    Returns:
        TUPLE -- returns condition variables and some contextes
    """
    all_chats = SendMessage.objects.filter(receiver=receiver)
    investor = get_role_service(name='investor')
    referee = get_role_service(name='referee')
    coach = get_role_service(name='coach')
    financial = get_role_service(name='financial')
    leader = get_role_service(name='leader')
    startup = models.User.objects.filter(user_type='startup')
    operational = get_role_service(name='operational')
    admin = models.User.objects.filter(Q(user_type='manager') |
                                       Q(is_admin=True))
    waiting = StartUp.objects.filter(
        status='select_not_presence_referees').count()
    not_presence_referee = StartUp.objects.filter(
        status='select_not_presence_referees').count()
    context.update({
        "all_chats": all_chats,
        'investor': investor,
        'referee': referee,
        'coach': coach,
        'financial': financial,
        'leader': leader,
        'subscriber': startup,
        'operational': operational,
        'admin': admin,
        'waiting': waiting,
        'not_presence_referee': not_presence_referee,
    })
    return tuple(context.values())



def dashboard_20_startups_services():
    """the last 20 startups to show to admins and coach
    
    Returns:
        QUERYSET -- returns a queryset of lastes startups in range of 20
    """
    return {'all_startups': StartUp.objects.all().order_by("-created_date")[:20]}


def dashboard_chart_service(investor ,coach ,leader ,referee ,operational, track_info):
    """get the numbers of karmand an the current year of chart
    
    Arguments:
        investor {OBJECT} -- the role of investor
        coach {OBJECT} -- the role of coach
        leader {OBJECT} -- the role of leader
        referee {OBJECT} -- the role of referee
        operational {OBJECT} -- the role of operational
    
    Returns:
        DICT -- returns the current year and all monthes of jalali and numbers of karmands
    """
    all_investorses = models.User.objects.filter(role=investor).count()
    all_startupses = StartUp.objects.all().count()
    all_coaches = models.User.objects.filter(role=coach).count()
    all_leaderes = models.User.objects.filter(role=leader).count()
    all_operationales = models.User.objects.filter(
        role=operational).count()
    all_referees = models.User.objects.filter(role=referee).count()
    th_year = JalaliDateTime.now().year
    chart = (StartUp.objects.filter(created_date__range=[get_date_jalali(int(th_year), month+1, 1), get_date_jalali(int(th_year), month+1, 31)]).count() for month in range(12))
    monthes = []
    
    for _ in range(12):
        monthes.append(chart.__next__())

    status = "وارد پنل مدیریت شد"
    status_of_user(track_info, status, 'import-dashboard-administrator')
    return {
    'farvardin': monthes[0],
    'ordi': monthes[1],
    'khurdad': monthes[2],
    'tir': monthes[3],
    'mordad': monthes[4],
    'shahrivar': monthes[5],
    'mehr': monthes[6],
    'aban': monthes[7],
    'azar': monthes[8],
    'daaay': monthes[9],
    'bahman': monthes[10],
    'esfand': monthes[11],
    'th_year': th_year,
    "all_investorses": all_investorses,
    "all_startupses": all_startupses,
    "all_coaches": all_coaches,
    "all_leaderes": all_leaderes,
    "all_operationales": all_operationales,
    "all_referees": all_referees}



def dashboard_ajax_chart_service(the_year):
    """get the specific year that given by ajax request
    
    Arguments:
        the_year {STRING} -- the specific year of jalali date
    
    Returns:
        JSONRESPONSE -- returns json of startups count in every month of jalali date
    """
    ajax_monthes=[]
    chart = (StartUp.objects.filter(created_date__range=[get_date_jalali(int(the_year), month+1, 1), get_date_jalali(int(the_year), month+1, 31)]).count() for month in range(12))
    for _ in range(12):
        ajax_monthes.append(chart.__next__())
    
    return {
                "country": "فروردین",
                "value": ajax_monthes[0],
            }, {
                "country": "اردیبهشت",
                "value": ajax_monthes[1],
            }, {
                "country": "خرداد",
                "value": ajax_monthes[2],
            }, {
                "country": "تیر",
                "value": ajax_monthes[3],
            }, {
                "country": "مرداد",
                "value": ajax_monthes[4],
            }, {
                "country": "شهریور",
                "value": ajax_monthes[5],
            }, {
                "country": "مهر",
                "value": ajax_monthes[6],
            }, {
                "country": "آبان",
                "value": ajax_monthes[7],
            }, {
                "country": "آذر",
                "value": ajax_monthes[8],
            }, {
                "country": "دی",
                "value": ajax_monthes[9],
            }, {
                "country": "بهمن",
                "value": ajax_monthes[10],
            }, {
                "country": "اسفند",
                "value": ajax_monthes[11],
            }



def dashboard_referee_service(track_info, user, search):
    """dashboard of users that have the role of referee
    
    Arguments:
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
        user {OBJECT} -- requested user
        search {DICT} -- a dictionary of values to search startups
    
    Returns:
        DICT -- returns dict of context
    """
    status = "وارد پنل داوران شد"
    status_of_user(track_info, status, 'import-dashboard-referee')

    th_referee = Referee.objects.filter(user=user, the_type='pres', scored=False)
    not_th_referee = Referee.objects.filter(
        user=user, the_type='not_pres', scored=False)
    referee_start = StartUp.objects.select_related('owner').filter(referee__in=th_referee)
    not_referee_start = StartUp.objects.select_related('owner').filter(referee__in=not_th_referee)

    if search.get('s_startup1'):
        referee_start = referee_start.filter(title__icontains=search.get('s_startup1'))
    if search.get('s_startup2'):
        not_referee_start = not_referee_start.filter(
            title__icontains=search.get('s_startup2'))
    return {"referee_start": referee_start,"not_referee_start": not_referee_start, "th_referee": th_referee, "not_th_referee": not_th_referee,}


def dashboard_leader_service(track_info):
    """show the startups that has been recommended to the requested user which has the leader role
    
    Arguments:
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
    
    Returns:
        DICT -- returns a queryset of events which will handle the ownership in template
    """
    leader_start = TheEvent.objects.prefetch_related('c_event').filter(
        th_type='leader').order_by('-created_date')
    status = "وارد پنل راهبران شد"
    status_of_user(track_info, status, 'import-dashboard-leader') 
    return {'leader_start': leader_start}


def dashboard_coach_service(track_info):
    """only track the coach for now ...
    
    Arguments:
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
    
    Returns:
        BOOLEAN -- if track goes successfully
    """
    status = "وارد پنل مربیان شد"
    status_of_user(track_info, status, 'import-dashboard-coach')
    return True


def dashboard_financial_service(track_info):
    """all the requests that made for any startup will be shown to user that has financial role
    
    Arguments:
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
    
    Returns:
        DICT -- returnd a dictionary of all Requests
    """
    the_requests = Requests.objects.all()
    status = "وارد پنل مالی شد"
    status_of_user(track_info, status, 'import-dashboard-financial')
    return {'the_requests': the_requests}


def dashboard_startup_service(user, track_info):
    """allow startup user to see Meeting coach event if it's not expired
       see all tracks for the owned startup
    
    Arguments:
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
    
    Returns:
        DICT -- returns contextes which contains the now time to check if the event expired and all events for meeting coach
    """
    status = "وارد پنل استارت اپ ها شد"
    status_of_user(track_info, status, 'import-dashboard-subscriber')
    the_event = TheEvent.objects.prefetch_related('c_event').filter(
        th_type='coach').order_by('-created_date')
    now_time = timezone.now()
    statuses = ['send-sms',
                'accept-first', 
                'fail-first', 
                'fail-referee-scores', 
                'fail-first_referee', 
                'fail-presence', 
                'fail-manage-request', 
                'fail-leader-request', 
                'fail-document', 
                'fail-referee-scores-pres',
                'accept-first',
                'accept-referee-scores',
                'accept-first_referee',
                'accept-presence',
                'accept-manage-request',
                'accept-leader-request',
                'accept-document',
                'submit-status-presence',
                'accept-referee-scores-pres',
                'select-leader',
                'import-information',
                'submit-scores',
                'submit-status-document',
                'select-not-presence-referees',
                'select-presence-referees',
                'selected-as-accelerator',]
    status = TheStatus.objects.filter(name__in=statuses)
    activities = UserTracker.objects.filter_by_model(instance=user.startup, the_status=status)
    return {"the_event": the_event, "now_time": now_time, 'activities': activities, 'statuses': statuses}


def dashboard_investor_service(user, invest_search, the_id, track_info, context):
    if user.can_see == True:
        invst_startups = StartUp.objects.filter(
            status='add_investor').prefetch_related('category').filter(category__in=user.category.all()).distinct()
        status = "وارد پنل سرمایه گذاران شد"
        status_of_user(track_info, status, 'import-dashboard-investor')

    else:
        invst_startups = StartUp.objects.filter(
            investor__user=user)
    
    if invest_search:
        invst_startups.filter(title__icontains=invest_search)
    return {'invst_startups': invst_startups}


def popup_request_service(id):
    """pass selected Request object to popup view
    
    Arguments:
        id {INT} -- to specify which Request record
    
    Returns:
        DICT -- returns a dictionary of selected Request object
    """
    return {"requst_popup": Requests.objects.get(pk=id), 'id': id}



# def profiles_service(id):
#     """select sepecifc user
    
#     Arguments:
#         id {INT} -- to specify which user to get info
    
#     Returns:
#         DICT -- returns info of user as dictionary
#     """
#     return {'the_profile': get_object_or_404(models.User, pk=id)}


# def get_user_by_phone_service(phone):
#     """allow users to login by their phone number 
#     in this type of login a verfication code will be sent to user number 
#     after the verification user will login automaticly
    
#     Returns:
#         OBJECT -- requested user
#     """
#     # return models.User.objects.get(phone=phone)
#     return get_user_service(phone=phone)


def validate_mobile_conditions_service(session):
    """check the time that user tried to login with phone to not allow user to spam
    
    Arguments:
        session {SESSOIN} -- to validate time in session with timezone now
    
    Returns:
        BOOLEAN -- returns True if everithing is valid else returns False
    """
    try:
        the_time = parser.parse(session['timer'])
    except:
        the_time = timezone.now()
    if 'timer' in session and the_time <= timezone.now():
        del session['timer']
    if 'timer' in session and the_time >= timezone.now():
        return False
    return True


def send_login_verification_service(the_user, track_info, session):
    """allow user to send sms every 2 minutes of tring to verify the sended
    
    Arguments:
        the_user {OBJECT} -- the requsted user information
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
        session {SESSION} -- to store timer and sended code for verification in next step and phone number
    
    Returns:
        BOOLEAN -- returns True if everythong go well :)
    """
    th_time = timezone.now() + timezone.timedelta(minutes=2)
    session['timer'] = str(th_time)
    random = str(randint(int('1' * 6), int('9' * 6)))
    session['the_code'] = random
    session['phone'] = the_user.phone
    sms.sms(random, the_user.phone, 'login')
    status = f'پیامک ارسال کد برای {the_user} ارسال شد'
    status_of_user(track_info, status, 'send-sms')
    create_notification(the_user, 'send-sms', the_user)
    return True


def login_verify_phone_service(the_code, expire_time, session, track_info):
    now = timezone.now()
    if expire_time >= now:
        if the_code == session.get('the_code'):
            # user = models.User.objects.get(
            #     phone=session.get('phone'))
            user = get_user_service(phone=session.get('phone'))
            del session['timer']
            del session['the_code']
            status = f"کاربر {user.first_name} {user.last_name} با شماره تلفن وارد شد"
            status_of_user(track_info, status, 'phone-login-dashboard')
            return (True, user,)
        else:
            return (False,)
    else:
        try:
            del session['the_code']
        except:
            pass
        try:
            del session['timer']
        except:
            pass
        return ('expired',)


def login_with_username_email_service(form, track_info):
    """allow user to login with username and email but don't allow user to login with phone number in this stage
       since the base login input is phone number
    
    Arguments:
        form {FORM} -- is a Form that contains 2 fields username and password
    
    Returns:
        BOOLEAN -- returns True if user login with phone number to throw an error else login user
    """
    username = form.cleaned_data.get('username')
    password = form.cleaned_data.get('password')
    if models.User.objects.filter(phone=username).exists():
        return 'exist'
    else:
        # try:
        user = authenticate(username=username, password=password)
        # finally:
        status = f"کاربر {username} وارد حساب کاربری خود شد"
        status_of_user(track_info, status, 'import-login-page')
        return user


def profile_mentor_service(search):
    """filter users that have the role of coach and leader and has chosen as mentor 
       and sort them by the number of their sort field
    
    Arguments:
        search {DICT} -- a dictionary of fullname search and category
    
    Returns:
        DICT -- returns querysets of mentors and categories
    """
    leader = get_role_service(name='leader')
    coach = get_role_service(name='coach')
    the_mentors = models.User.objects.filter(Q(role=leader) | Q(
        role=coach), add_to_mentors=True).distinct().order_by('sort')
    categories = Categories.objects.all()

    if search.get('full_search'):
        the_mentors = the_mentors.filter(
            Q(first_name__icontains=search.get('full_search')) | Q(last_name__icontains=search.get('full_search')))
    if search.get('cats'):
        the_mentors = the_mentors.filter(category=search.get('cats'))
    return {'the_mentors': the_mentors, "categories": categories}


def sort_mentors_service():
    """filter users that has been chosen as mentors and order them by their sort number
    
    Returns:
        QUERYSET -- returns queryset of users
    """
    return models.User.objects.filter(add_to_mentors=True).order_by('sort')


def sort_mentors_sort_service(the_mentors, user_sort_num, track_info):
    """for every mentors gets the number of the sorted input and assign them to the user 
    
    Arguments:
        the_mentors {QUERYSET} -- a queryset of users that has been chosen as
        user_sort_num {LIST} -- the list of numbers that will assgin to users in every change in their place
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
    
    Returns:
        BOOLEAN -- returns True if everythig goes well
    """
    for user in the_mentors:
        for sort in user_sort_num.getlist(f"sort_{user.pk}"):
            user.sort = int(sort)
            user.save()
            create_notification(user, 'sorted-mentor', user)
    status = f"لیست منتور ها تغییر کرد"
    status_of_user(track_info, status, 'sorted-mentor')
    return True



def admin_form_profile_service(user, track_info, context):
    """get the form that only for admins
    
    Arguments:
        user {OBJECT} -- requested user
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
    
    Returns:
        FORM -- returns admin form that belongs to requested user
    """
    admin_form = ProfileAdminForm(instance=user)
    status = f"{admin_form.instance.first_name} {admin_form.instance.last_name} وارد صفحه پروفایل خود شد"
    status_of_user(track_info, status, 'import-profile')
    context.update({'admin_form': admin_form})
    return admin_form


def admin_form_fill_service(user, form, track_info):
    """allow user to chage his profile informations
    
    Arguments:
        user {OBJECT} -- requested user
        form {POST Method} -- to get birthdate and define date of form
    
    Returns:
        BOOLEAN -- returns True if forn is valid
    """
    admin_form = ProfileAdminForm(form, instance=user)
    if admin_form.is_valid():
        lists = get_list(form['birth_date'])
        date = JalaliDate(lists[0], lists[1], lists[2]).to_gregorian()
        admin_form.instance.birth_date = date
        admin_form.instance.is_compeleted = True
        admin_form.save()

        status = f"{admin_form.instance.first_name} {admin_form.instance.last_name} را تغییر داد"
        status_of_user(track_info, status, 'import-profile')
        return True
    elif models.User.objects.filter(email=form.get('email')):
        logger.error(str(admin_form.errors))
        return "exists"
    else:
        logger.error(str(admin_form.errors))
        return "failed"


def role_form_profile_service(user, track_info, context):
    """get the instance form of the requested user which is a karmand
    
    Arguments:
        user {OBJECT} -- requested user
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
    
    Returns:
        FORM -- returns form instance that blogs to the requested user
    """
    role_form = ProfileRoleForm(instance=user)
    status = f"{role_form.instance.first_name} {role_form.instance.last_name} وارد صفحه پروفایل خود شد"
    status_of_user(track_info, status, 'import-profile')
    context.update({'role_form': role_form})
    return role_form


def edit_role_profile_service(form, file_value, user, track_info):
    """allow user to edit his/her profile
    
    Arguments:
        form {POST Method} -- get some values from user
        file_value {FILES} -- allow user to upload files
        user {OBJECT} -- requested user
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
    
    Returns:
        BOOLEAN/STRING -- returns True if form is valid if email exists returns exists else return failed
    """
    role_form = ProfileRoleForm(
        form, file_value, instance=user)

    if role_form.is_valid():
        lists = get_list(form['birth_date'])
        date = JalaliDate(lists[0], lists[1], lists[2]).to_gregorian()
        role_form.instance.birth_date = date
        try:
            image_b64 = form.get('avatar_base64')
            th_img , ext = resize_pics(image_b64)
            role_form.instance.avatar.save(f'user.{ext}', files.File(th_img), save=False)
        except:
            pass
        role_form.instance.is_compeleted = True

        role_form.save()
        status = f"{role_form.instance.first_name} {role_form.instance.last_name} را تغییر داد"
        status_of_user(track_info, status, 'edit-profile')
        return True
    elif models.User.objects.filter(email=form.get('email')).exists():
        logger.error(str(role_form.errors))
        return 'email_exists'
    else:
        logger.error(str(role_form.errors))
        return 'failed'