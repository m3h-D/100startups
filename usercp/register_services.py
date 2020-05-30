from startups.engine import sms
from random import randint
from django.utils import timezone
from .forms import *
from dateutil import parser
from startups.utils import *
from startup.models import *
from category.models import Categories
from startups.object import get_startup_service, get_user_service, get_role_service
from startup.models import StartUp
from startup.forms import *
from . import models
from persiantools.jdatetime import JalaliDate, JalaliDateTime
from django.core import files
from threading import Thread
import re
import logging

logger = logging.getLogger(__name__)

def send_sms_again_service(session):
    """get the phone number that stored in session in stage of 1 and calculate random number and send that as sms
    
    Arguments:
        session {SESSION} -- to store and check phone and validation code
    
    Returns:
        BOOLEAN -- returns True if everythig goes well
    """
    phone = session.get('phone')
    sms_validate = str(randint(int('1' * 6), int('9' * 6)))
    session['sms_validate'] = sms_validate
    sms.sms(sms_validate, phone, 'register')
    t_register = timezone.now() + timezone.timedelta(minutes=2)
    session['register_timer'] = str(t_register)
    return True


def register_user_condition_service(session, phone_form, form):
    """checks if user can register
       - if the number assigned to a user that has role cannot create startup
       - user only can request for verification code every 2 minutes
       -
    
    Arguments:
        session {SESSION} -- to store generated code/ registered time
        phone_form {POST Method} -- get the number that user has entered
        form {FORM} -- to validate number that has been entered
    
    Returns:
        STRING -- if try to spam returns expired if is karmand return karmand return error if not valid
    """
    try:
        the_time = parser.parse(session['register_timer'])
    except:
        the_time = timezone.now()

    if the_time <= timezone.now():
        try:
            del session['register_timer']
        except:
            pass

        try:
            del session['sms_validate']
        except:
            pass

    if 'register_timer' in session and the_time >= timezone.now():
        return 'expired'
    else:
        
        register_t = timezone.now() + timezone.timedelta(minutes=2)
        try:
            th_user = get_user_service(phone=phone_form.get('phone'))
            if th_user.user_type == 'karmand':
                return 'karmand'

            session['phone'] = phone_form.get('phone')
            sms_validate = str(randint(int('1' * 6), int('9' * 6)))
            sms.sms(sms_validate, session['phone'], 'register')
            session['sms_validate'] = sms_validate
            session['register_timer'] = str(register_t)
            return 'success'
        except:
            if form.is_valid():
                session['phone'] = form.cleaned_data['phone']
                sms_validate = str(randint(int('1' * 6), int('9' * 6)))
                sms.sms(sms_validate, session['phone'], 'register')
                session['sms_validate'] = sms_validate
                session['register_timer'] = str(register_t)
                return 'success'
            else:
                print(str(form.errors))
                return 'error'

    



def verify_user_service(session, form):
    """check the verification code if time is not expire / if user exists will login or create user then login 
    
    Arguments:
        session {SESSION} -- to check verification code and time
        form {POST method} -- with one field to get code
    
    Returns:
        STRING -- returns loggedin and user if goes successfully/expire if time remain to send again / false if code is wrong
    """
    the_time = parser.parse(session['register_timer'])

    if the_time >= timezone.now():

        if str(form['verify']) == str(session['sms_validate']):
            
            try:
                user = get_user_service(phone=session['phone'])
            except:
                username_random, password = create_passwd()
                user = models.User.objects.create_startup_user(
                    phone=session['phone'], password=password, username=username_random)
                UserProfile.objects.create(user=user)
                session['the_startup_user_password'] = str(password)
            
            return ('loggedin', user)
        else:
            return 'false'
    else:
        try:
            del session['sms_validate']
        except:
            pass
        if not 'sms_validate' in session:
            return 'expired'


def verify_user_track_user(session, track_info, user):
    """track user if goes to verify page
    
    Arguments:
        session {SESSION} -- to store phone and delete register_time
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
        user {OBJECT} -- requested user
    
    Returns:
        BOOLEAN -- returns True if everithing goes well
    """
    if user.step == 'finish':
        return False
    else:
        session['phone'] = user.phone
        status = f"وارد صفحه اعتبار سنجی شد {session.get('phone')}"
        status_of_user(track_info, status, 'import-verify-step')
        try:
            del session['register_timer']
        except KeyError:
            pass
        return True


def fetch_startup_service(owner, context):
    """get the startup that assign to the requested user and get the custom leader that added by user
    
    Arguments:
        owner {OBEJCET} -- requested user
        context {DICT} -- a dictionary of context to add it some more context
    
    Returns:
        OBJECT -- returns the determined startup
    """
    db_startup = get_startup_service(owner=owner)
    the_time = JalaliDateTime.now().to_gregorian()
    try:
        user_mentor = get_startup_service(
            owner=owner, rahbar__mentor_user=True)
    except:
        user_mentor = None
    
    context.update({
            'the_time': the_time,
            'user_mentor': user_mentor,
            'db_startup': db_startup,
        })
    
    return db_startup


def update_startup_service(form, file_value, user, track_info, form_start):
    """if request method is POST and the startup is already exists it will allow to update it
    
    Arguments:
        form {POST Method} -- to get some fileds for  category and so on
        file_value {FILES} -- get the imported files (image)
        user {OBJECT} -- requested user
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
        form_start {FORM} -- get the model form that has instances of current startup
    
    Returns:
        BOOLEAN -- returns True if form is valid
    """
    if form_start.is_valid():
        lists = get_list(form['start_date1'])
        date = JalaliDate(lists[0], lists[1], lists[2]).to_gregorian()
        form_start.instance.start_date = date
        form_start.instance.site = form.get('site') if form.get('site').startswith('http') else str('http://') + str(form.get('site'))
        try:
            image_b64 = form.get('avatar_base64')
            th_img , ext = resize_pics(image_b64)
            form_start.instance.image.save(f'startup.{ext}', files.File(th_img), save=False)
        except:
            pass
        if form_start.instance.status == 'failed_document':
            form_start.instance.status = 'editing'
            form_start.save()
            the_c = StartupComments.objects.get(
                startup=form_start.instance)
            the_c.doc_stat = None
            the_c.doc_stat_status = None
            the_c.save()

        if form_start.instance.status == 'failed':
            form_start.instance.status = 'editing'
            form_start.save()
            the_c = StartupComments.objects.get(
                startup=form_start.instance)
            the_c.startup_stat = None
            the_c.startup_stat_status = None
            the_c.save()

        form_start.instance.category.clear()
        for cat in form.getlist('category'):
            form_start.instance.category.add(cat)

        form_start.save()
        user_profile = UserProfile.objects.get(
            user=user)
        user_profile.startup = form_start.instance
        user_profile.save()
        if user_profile.user.step == 'startup':
            user_profile.user.step = 'team'
            user_profile.user.save()
        status = f"استارت اپ {form_start.instance.title} را تغییر داد"
        status_of_user(track_info, status, 'registering-startup-step')
        return True
    else:
        logger.error(str(form_start.errors))


def track_startup_creation_service(track_info):
    """only to track user
    
    Arguments:
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
    
    Returns:
        BOOLEAN -- returns True if it saves the status of user
    """
    status = f"وارد مرحله استارت اپ شد"
    status_of_user(track_info, status, 'import-startup-step')
    return True


def startup_create_service(form, file_value, user, track_info, form_start):
    """allow user to create fresh startup
    
    Arguments:
        form {POST Method} -- to get some values
        file_value {FILES} -- to get image
        user {OBJECT} -- requested user
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
        form_start {FORM} -- to save the entered data to the StartUp tabel
    
    Returns:
        [type] -- [description]
    """
    if form_start.is_valid():
        lists = get_list(form['start_date1'])
        date = JalaliDate(lists[0], lists[1], lists[2]).to_gregorian()
        form_start.instance.start_date = date
        form_start.instance.site = form.get('site') if form.get('site').startswith('http') else str('http://') + str(form.get('site'))
        form_start.instance.owner = user
        form_start.instance.owner.step = 'team'
        form_start.instance.owner.save()
        form_start.instance.status = 'not_complete'
        form_start.save()

        form_start.instance.category.clear()
        for cat in form.getlist('category'):
            form_start.instance.category.add(cat)
        try:
            image_b64 = form.get('avatar_base64')
            th_img , ext = resize_pics(image_b64)
            form_start.instance.image.save(f'startup.{ext}', files.File(th_img), save=False)
        except:
            pass
        form_start.save()

        status = f"استارت اپ {form_start.instance.title} را ثبت کرد"
        status_of_user(track_info, status, 'registering-startup-step')

        user_profile = UserProfile.objects.get(
            user=user)
        user_profile.startup = form_start.instance
        user_profile.save()
        user_profile.user.step = 'team'
        user_profile.user.save()
        return True
    else:
        logger.error(str(form_start.errors))


def assign_accelerator_or_leader(user, form, form_start):
    """allow user to choose a leader o accelerator or create custom leader(mentor)
    
    Arguments:
        user {OBJECT} -- requested user
        form {POST Method} -- to get values from user
        form_start {FORM} -- to assign selected options (leader, accelerator) to the current startup
    
    Returns:
        BOOLEAN -- returns False if user use his/her phone number to create a mentor/ True if everythig goes well 
    """
    if user.phone in form.getlist('mentor_number'):
        return False
    else:
        try: # user create a custome leader and it will add to startup rahbar
            user_mentor = get_user_service(
                first_name=form['mentor_fname'],
                last_name=form['mentor_lname'],
                phone=form['mentor_number'],
            )
            form_start.instance.rahbar = user_mentor
            form_start.save()
        except:
            if form.getlist('mentor_fname') and form.getlist('mentor_lname') and form.getlist('mentor_number'):
                username_random, password = create_passwd()
                try:
                    user_mentor = get_user_service(
                        phone=form['mentor_number']
                    )
                    form_start.instance.rahbar = user_mentor
                    form_start.save()
                except:
                    user_mentor = models.User.objects.create(
                        first_name=form['mentor_fname'],
                        last_name=form['mentor_lname'],
                        phone=form['mentor_number'],
                        is_active=False,
                        username=username_random,
                        mentor_user=True,
                    )
                    user_mentor.set_password(password)
                    form_start.instance.rahbar = user_mentor
                    role = get_role_service(name='leader')
                    user_mentor.role.add(role)
                    form_start.save()
                    if form_start.instance.shetab_dahande:
                        form_start.instance.shetab_dahande = None
                        form_start.instance.shetab_shude = False
                        form_start.save()

        if form.getlist('companion1'): # get shetabdahande and add namayande as rahbar_asli for startup
            for person_id in form.getlist('companion1'):
                if not re.search(r'\d', person_id, re.I):
                    continue
                shetab_dahande = ShetabDahande.objects.get(
                    pk=int(person_id))
                form_start.instance.shetab_dahande = shetab_dahande
                form_start.instance.rahbar_asli = shetab_dahande.name_namayande
                form_start.instance.rahbar = None
                form_start.instance.shetab_shude = True
                form_start.save()
        if form.getlist('mentor_name'): # user choose a leader and it will add to startup rahbar
            for person_id in form.getlist('mentor_name'):

                if not person_id:
                    continue
                user_rahbar = get_user_service(
                    pk=int(person_id))
                form_start.instance.rahbar = user_rahbar
                form_start.save()
                if form_start.instance.shetab_dahande:
                    form_start.instance.shetab_dahande = None
                    form_start.instance.shetab_shude = False
                    form_start.save()
        return True


def team_instance_service(user, context, trak_info):
    """get the requested user info / startup/ team members if available
    
    Arguments:
        user {OBJECT} -- requsted user
        context {DICT} -- a dictionary to assign more contextes
    
    Returns:
        TUPLE -- returns tuple of context valuse to use the in page
    """
    teams = TeamMember.objects.filter(
        pk__in=user.userprofile.team_member.all())
    leader_form = LeaderUserForm(instance=user)
    userprofile_form = LeaderForm(instance=user.userprofile)
    db_startup = get_startup_service(owner=user)
    form_start = StartUpForm5(instance=db_startup)

    status = f"وارد مرحله تیم استارت اپ {db_startup.title} شد"
    status_of_user(trak_info, status, 'import-team-step')
    context.update({'teams': teams,
                    'leader_form': leader_form,
                    'userprofile_form': userprofile_form,
                    'form_start': form_start,
                    'db_startups': db_startup})
    return db_startup


def fill_team_info_service(form, file_value, leader_form, form_start, userprofile_form, user, trak_info, db_startup):
    """allow user to fill information about self and add team mates for the startup 
    
    Arguments:
        form {POST Method} -- get list or single valuse from user
        file_value {FILE} -- get the resume files to assign to team  mates
        leader_form {FORM} -- instance of user info that connected to User model
        form_start {FORM} -- instance of startup info that connected to StartUp model
        userprofile_form {FORM} -- instance of user info that connected to UserProfile model
        user {OBJECT} -- requested user
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
        db_startup {OBJECT} -- the startup that requested user owns it
    
    Returns:
        BOOLEAN -- returns True if forms are valid
    """
    if leader_form.is_valid() and form_start.is_valid() and userprofile_form.is_valid():
        the_list = get_list(form['birth_date'])
        owener_birth_date = JalaliDate(
            the_list[0], the_list[1], the_list[2]).to_gregorian()
        leader_form.instance.birth_date = owener_birth_date
        userprofile_form.save()
        form_start.save()

        if userprofile_form.instance.team_member:
            userprofile_form.instance.team_member.clear()
        if leader_form.instance.step == 'team':
            leader_form.instance.step = 'upload'
            leader_form.save()
        leader_form.save()
        index_of_pdf = (i for i in file_value.getlist('cv[]'))
        index_of_avatar = (i for i in file_value.getlist('t_avatar[]'))
        for i in range(len(form.getlist('email_l[]'))):
            if not form.getlist('first_namel[]')[i]:
                continue
            lists = get_list(form.getlist('birthdayl[]')[i])
            date = JalaliDate(
            lists[0], lists[1], lists[2]).to_gregorian()
            try:
                if form.getlist('team_id')[i]:
                    team = TeamMember.objects.get(pk=form.getlist('team_id')[i])
                    team.t_first_name = form.getlist('first_namel[]')[i]
                    team.t_last_name = form.getlist('last_namel[]')[i]
                    team.t_phone = form.getlist('mobilel[]')[i]
                    team.t_email = form.getlist('email_l[]')[i]
                    team.t_birth_date = date
                    team.tgrade = form.getlist('educationl1[]')[i]
                    team.t_the_role = form.getlist('sidel[]')[i]
                    team.t_duration_per_month = form.getlist('averagel[]')[i]
                    team.t_saham = form.getlist('stockl[]')[i]
                    team.t_skill = form.getlist('expertisel[]')[i]
                    team.t_role_in_startup = form.getlist('role[]')[i]
                    team.save()
                    try:
                        team.t_linkdin=form.getlist('linkdinl[]')[i]
                        team.save()
                    except:
                        pass

                    if form.getlist('cv_index')[i] == str(1):
                        team.t_cv = index_of_pdf.__next__()
                        team.save()

                    if form.getlist('avatar_index')[i] == str(1):
                        team.t_avatar = index_of_avatar.__next__()
                        team.save()

                    userprofile_form.instance.team_member.add(team)


            except:
                team = TeamMember.objects.create(
                    startup=user.startup,
                    t_first_name=form.getlist('first_namel[]')[i],
                    t_last_name=form.getlist('last_namel[]')[i],
                    t_phone=form.getlist('mobilel[]')[i],
                    t_email=form.getlist('email_l[]')[i],
                    t_birth_date=date,
                    tgrade=form.getlist('educationl1[]')[i],
                    t_the_role=form.getlist('sidel[]')[i],
                    t_duration_per_month=form.getlist('averagel[]')[i],
                    t_saham=form.getlist('stockl[]')[i],
                    t_skill=form.getlist('expertisel[]')[i],
                    t_role_in_startup=form.getlist('role[]')[i],
                )
                try:
                    team.t_linkdin=form.getlist('linkdinl[]')[i]
                    team.save()
                except:
                    pass

                if form.getlist('cv_index')[i] == str(1):
                    team.t_cv = index_of_pdf.__next__()
                    team.save()

                if form.getlist('avatar_index')[i] == str(1):
                    team.t_avatar = index_of_avatar.__next__()
                    team.save()

                userprofile_form.instance.team_member.add(team)
            if form_start.instance.status == 'failed_document':
                form_start.instance.status = 'editing'
                form_start.save()
                the_c = StartupComments.objects.get(
                    startup=form_start.instance)
                the_c.doc_stat = None
                the_c.doc_stat_status = None
                the_c.save()

            if form_start.instance.status == 'failed':
                form_start.instance.status = 'editing'
                form_start.save()
                the_c = StartupComments.objects.get(
                    startup=form_start.instance)
                the_c.startup_stat = None
                the_c.startup_stat_status = None
                the_c.save()
        
        status = f"اطلاعات راهبر و تیم ساخته استارت اپ {db_startup.title} شد/تغییر کرد"
        status_of_user(trak_info, status, 'submit-team-step')
        return True
    else:
        return False


def remove_team_member_service(form):
    """get the id from form and delete the selected team memeber 
    
    Arguments:
        form {POST Method} -- get the id from ajax
    
    Returns:
        DICT -- returns the deleted team member id
    """
    acc_id = form.get('post_idss')
    person = TeamMember.objects.get(pk=acc_id)
    person.delete()
    data = {
        'post_idss': acc_id,
    }
    return data


def upload_video_service(owner, track_info):
    """allow user to upload a vidoe to add more info about him/her startup
    
    Arguments:
        owner {OBJECT} -- requested user
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
    
    Returns:
        FORM -- returns instance of startup form
    """
    db_startup = get_startup_service(owner=owner)
    status = f"وارد صفحه اپلود استارت اپ {db_startup.title} شد"
    status_of_user(track_info, status, 'import-upload-step')
    form = StartUpForm2(instance=db_startup)
    return db_startup ,form


def uploaded_video_service(form, track_info, db_startup):
    """get the video and save it for current users startup and set user step for the next stage
    
    Arguments:
        form {FORM} -- a form to store video
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
        db_startup {OBJECT} -- current users startup
    
    Returns:
        BOOLEAN -- retursn True if everything goes well
    """
    status = f"ویدیو استارت اپ {form.instance.title} بارگذاری شد"
    status_of_user(track_info, status, 'submit-upload-step')
    if form.is_valid():
        form.save()
        if form.instance.status == 'failed_document':
            form.instance.status = 'editing'
            form.save()
            the_c = StartupComments.objects.get(
                startup=form.instance)
            the_c.doc_stat = None
            the_c.doc_stat_status = None
            the_c.save()

        if form.instance.status == 'failed':
            form.instance.status = 'editing'
            form.save()
            the_c = StartupComments.objects.get(
                startup=form.instance)
            the_c.startup_stat = None
            the_c.startup_stat_status = None
            the_c.save()
        if db_startup.owner.step == 'upload':
            db_startup.owner.step = 'presentation'
            db_startup.owner.save()
    else:
        logger.error(str(form.errors))
    return True



def presentation_service(owner, track_info):
    """get the current users startup and a form with startup instance
    
    Arguments:
        owner {OBJECT} -- requested user
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
    
    Returns:
        FORM -- returns startup instances as form
    """
    db_startup = get_startup_service(owner=owner)
    status = f"وارد صفحه پیج دک استارت اپ {db_startup.title} شد"
    status_of_user(track_info, status, 'import-presentation-step')
    startup_form = StartUpForm3(instance=db_startup)
    return startup_form, db_startup


def presentation_text_services(startup_form, form, session, track_info):
    """user will fill some information
    
    Arguments:
        startup_form {FORM} -- get startup form that belongs to requested uesr
        form {POST Method} -- to get require_money as string and converting it as integer
        session {SESSION} -- to get user phone if it's deleted for the next stage
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
    
    Returns:
        BOOLEAN -- returns True if form is valid
    """
    if startup_form.is_valid():
        startup_form.instance.require_money = int(
            ''.join(form.get('require_money').split(',')))
        startup_form.save()
        if startup_form.instance.status == 'failed_document':
            startup_form.instance.status = 'editing'
            startup_form.save()
            the_c = StartupComments.objects.get(
                startup=startup_form.instance)
            the_c.doc_stat = None
            the_c.doc_stat_status = None
            the_c.save()

        if startup_form.instance.status == 'failed':
            startup_form.instance.status = 'editing'
            startup_form.save()
            the_c = StartupComments.objects.get(
                startup=startup_form.instance)
            the_c.startup_stat = None
            the_c.startup_stat_status = None
            the_c.save()
        if startup_form.instance.owner.step == "presentation":
            startup_form.instance.owner.step = "finish"
            startup_form.instance.owner.save()
        status = "پیچ دک استارت اپ ساخته شد/تغییر کرد"
        status_of_user(track_info, status, 'submit-presentation-step')
        session['phone'] = startup_form.instance.owner.phone
        return True
        
    else:
        logger.error(str(startup_form.errors))


def presentation_instance_file(id, th_file):
    """get the startup finance forecast/ peachdeck file if available
    
    Arguments:
        id {INT} -- the id of the chosen startup
        th_file {STRING} -- check if the file is for pdeck or finance forecast
    
    Returns:
        TUPLE -- returns db_startup objects and startup from 
    """
    db_startup = get_startup_service(pk=id)
    if th_file == 'mali':
        startup_form = StartUpForm6(instance=db_startup)
    elif th_file == 'pgdeck':
        startup_form = StartUpForm4(instance=db_startup)
    return db_startup, startup_form

def presentation_files_save(startup_form):
    """attach files to startup
    
    Arguments:
        startup_form {FORM} -- get the form for each file
    
    Returns:
        BOOLEAN -- returns True if everything goes well
    """
    if startup_form.is_valid():
        startup_form.save()
    else:
        logger.error(str(startup_form.errors))
    return True


def finish_service(user, session, track_info):
    """when user reach to this stage the status of startup will be change to pending
       and some emails will be sent to startups owner, leader, team members, accelerator
    
    Arguments:
        user {OBJECT} -- requested user
        session {SESSION} -- to get user phone if it's deleted for the next stage
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
    
    Returns:
        BOOLEAN -- returns True if everything goes well
    """

    the_startup = get_startup_service(owner=user)
    if the_startup.status in ('pending', 'not_complete'):
        the_startup.status = 'pending'
        the_startup.save()
    to = the_startup.owner.email
    if not "email_sent" in session:
        template = 'email/active_email.html'
        the_message = f"""
مدیر محترم تیم {user.first_name} {user.last_name} 
از اینکه طرح خود را در سامانه 100استارت‌آپ ثبت کردید متشکریم، شما می‌توانید وضعیت تیم خود را از سامانه پیگیری نمایید.
"""
        sub = 'ثبت استارت آپ'

        Thread(target=send_email, args=(track_info,), kwargs={
            "to": [to] , 'first_name': user.first_name,'last_name': user.last_name, 'template': template, 'sub': sub, 'the_messages': the_message}).start()
        for x in TeamMember.objects.filter(startup=the_startup):
            if not x.t_email:
                continue
            sub = 'عضویت در استارت اپ'
            the_message = """سلام
استارتاپ شما در سامانه 100استارت‌آپ به ثبت رسیده است، امیدواریم با همراهی هم، بتوانیم مسیر موفقیت را به سرعت طی کنیم."""
            Thread(target=send_email, args=(track_info,), kwargs={
                "to": [x.t_email], 'first_name': x.t_first_name,'last_name': x.t_last_name , 'is_team': True, 'template': template, 'sub': sub, 'the_messages': the_message}).start()
        if the_startup.rahbar:
            sub = 'راهبر پیشنهادی استارت اپ'
            the_message = f"""راهبر گرامی، {the_startup.rahbar.first_name} {the_startup.rahbar.last_name} 
تیم {the_startup.title}طرح خود را در سامانه 100استارت‌آپ ثبت نموده‌است،
و شما بعنوان راهبر می‌توانید وضعیت این تیم را از سامانه پیگیری نمایید.
امیدواریم با کمک های شما مسیر سخت موفقیت هموار شود.
ممنون از همراهیتان
"""
            Thread(target=send_email, args=(track_info,), kwargs={
                "to": [the_startup.rahbar.email], 'is_team': True, 'first_name': the_startup.rahbar.first_name,'last_name': the_startup.rahbar.last_name , 'template': template, 'sub': sub, 'the_messages': the_message}).start()
        elif the_startup.rahbar_asli:
            sub = 'راهبر پیشنهادی استارت اپ'
            the_message = f"""شتابدهنده محترم {the_startup.rahbar_asli.first_name} {the_startup.rahbar_asli.last_name} 
تیم {the_startup.title} طرح خود را در سامانه 100استارت‌آپ ثبت نموده‌است،
و شما بعنوان شتابدهنده می‌توانید وضعیت این تیم را از سامانه پیگیری نمایید.
ممنون از همراهیتان"""
            Thread(target=send_email, args=(track_info,), kwargs={
                "to": [the_startup.rahbar_asli.email], 'is_team': True, 'first_name': the_startup.rahbar_asli.first_name,'last_name': the_startup.rahbar_asli.last_name , 'template': template, 'sub': sub, 'the_messages': the_message}).start()
        session['email_sent'] = True
        status = "پایان ثبت استارت اپ و ارسال ایمیل"
        status_of_user(track_info, status, 'import-finish-step')
    return True