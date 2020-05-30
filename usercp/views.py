from io import BytesIO
from django.core import files
import requests
from urllib.request import urlopen
from dateutil import parser
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from random import randint
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth import authenticate, logout, login as auth_login

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import uuid
import pickle
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
                          LoginForm,
                          )
from django.contrib.auth.decorators import login_required
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

from startups.utils import *
from . import models
from category.models import Categories
from startup.models import StartUp, ShetabDahande, StartupComments, TeamMember, Referee, Requests, Investors, UserProfile
from message.models import SendMessage
from theevent.models import TheEvent
from usertracker.models import UserTracker, TheStatus
import logging

import os
from startups import settings

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token

from .dashboard_services import *
from .register_services import *
from django.contrib.sites.shortcuts import get_current_site
from urllib.parse import urlsplit


logger = logging.getLogger(__name__)


def all_logs(request):
    """[open mylog.log to show all requsets to site in html, if user is superuser]
    
    Arguments:
        request {[GET]} -- [show every requests to site]
    
    Returns:
        [DICT] -- [every logs stored in mylogs.log linear]
    """
    if request.user.is_admin:
        the_logs = []
        with open(os.path.join(settings.BASE_DIR, 'logs/mylog.log'), 'r') as f:
            for line in f:
                the_logs.append(line)
        return render(request, 'logs.html', {'the_logs': the_logs})
    else:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def url_logs(request):
    """[open django_request.log to show all requsets to urls in html, if user is superuser]
    
    Arguments:
        request {[GET]} -- [show every requests to urls]
    
    Returns:
        [DICT] -- [every logs stored in django_request.log linear]
    """
    if request.user.is_admin:
        the_logs = []
        with open(os.path.join(settings.BASE_DIR, 'logs/django_request.log'), 'r') as f:
            for line in f:
                the_logs.append(line)
        return render(request, 'logs2.html', {'the_logs': the_logs})
    else:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))



@logging_view
def redirect_url_to_register(request):
    """[redirect to dashboard or register rout depend if user is authenticated or not]
    
    Arguments:
        request {[GET]} -- [status of requested user]
    
    Returns:
        [URL] -- [redirect to register or dashboard]
    """
    if request.user.is_authenticated:
        return redirect('usercp:dashboard_panel')
    return redirect('usercp:register')


@logging_view
# @user_tracker()
def forget_password(request):
    """a view that takes username or email and send a token to the requested user email to set new password
    
    Arguments:
        request {REQUEST} -- requested user info
    
    Returns:
        RENDER -- render forget password tempalte
    """
    if request.method == "POST":
        form = request.POST
        protocol = urlsplit(request.build_absolute_uri(None)).scheme
        current_site = get_current_site(request)
        succeeded = forget_password_service(request.track_info, form, protocol, current_site)
        if succeeded:
            messages.success(request, 'لینک فراموشی برای ایمیل شما ارسال شد', extra_tags='forget_password_compeleted')
        else:
            messages.warning(request, 'چنین ایمیل یا نام کاربری موجود نیست', extra_tags='no_user_email_forget')
    return render(request, 'usercp/panel/forget-password.html')



@logging_view
# @user_tracker()
def new_password(request, uidb64, token):
    """user can set new password for their account 
    
    Arguments:
        request {REQUEST} -- requested user
        uidb64 {STRING} -- hashed user ii
        token {TOKEN} -- random hashed str from user info
    
    Returns:
        RENDER -- render the new_password page if the token and uidb64 is valid
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = get_user_service(pk=uid)
    except(TypeError, ValueError, OverflowError, models.User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        if request.method == "POST":
            form = request.POST
            if new_password_service(form, user):
                messages.warning(request, 'asd', extra_tags='password_changed')
                return redirect('usercp:login')
            else:
                messages.warning(request, 'مشکلی در تغییر رمزعبور پیش آمد', extra_tags='password_changed_failed')
    else:
        return HttpResponse('لینک نا معتبر است.')
    return render(request, 'usercp/panel/new-password.html')


@logging_view
@login_required(login_url='usercp:login')
# @user_tracker()
def change_password(request):
    """allow user to change his/her password without logingout
    
    Arguments:
        request {REQUEST} -- requested user
    
    Returns:
        RENDER -- if user is authenticated render change-password html
    """
    form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if change_password_service(form, request.track_info):
            update_session_auth_hash(request, request.user)
            return HttpResponseRedirect('/profile/')
        else:
            logger.error(str(form.errors))
            messages.error(
                request, 'Your password was not successfully updated!', extra_tags='changing_password')

    return render(request, 'usercp/panel/change-password.html', {'form': form})


@logging_view
@login_required(login_url='usercp:login')
# @user_tracker()
def change_username(request):
    """allow user to change his/her username if the mentioned username is not exists
    
    Arguments:
        request {REQUEST} -- requested user
    
    Returns:
        RENDER -- render the change-username html
    """
    if request.method == "POST":
        form = request.POST
        if change_username_service(form, request.track_info, request.user):
            return HttpResponseRedirect('/profile/')
        else:
            messages.warning(request, 'این نام کاربری موجود است', extra_tags='username_exists')
    return render(request, 'usercp/panel/change-username.html')


@logging_view
@login_required(login_url='usercp:login')
@premession(th_type1='manager',  role=['operational', ])
# @user_tracker(model='user')
def create_user(request):
    """a form to create user(only the users with type of Karmand)
    
    Arguments:
        request {REQUEST} -- for the render
    
    Returns:
        RENDER -- returns the html if requested user has premession
    """
    user_form, roles, categories = create_user_get_service(request.track_info)

    if request.method == "POST":
        form = request.POST
        if create_user_post_service(user_form, form, request.track_info) == True:
            messages.warning(request, 'asd', extra_tags='success_user')
            return redirect('usercp:list_user')
        else:
            messages.warning(request, 'asd', extra_tags=create_user_post_service(user_form, form, request.track_info))
    return render(request, 'usercp/panel/create-user.html', {'user_form': user_form, 'categories': categories, 'roles': roles})



@logging_view 
@login_required(login_url='usercp:login')
@premession(th_type1='manager',  role=['operational'])
# @user_tracker()   
def list_user(request):
    """list of all users depends of requested user premession and search
    
    Arguments:
        request {REQUEST} -- used to get values from search boxes and check requested user
    
    Returns:
        RENDER -- render list-user.html if the requested user has required premesson
    """
    search_query = {
    'role_input': request.GET.get('role'),
    'fname': request.GET.get('fname_search'),
    'lname': request.GET.get('lname_search'),
    'email': request.GET.get('email_search'),
    'the_phone': request.GET.get('phone'),
    'offset': request.GET.get('page')
    }
    context = list_user_service(search_query, request.track_info)
    return render(request, 'usercp/panel/list-user.html', context)


@login_required(login_url='usercp:login')
# @user_tracker()
def delete_user(request):
    """delete specific user by ajax request
    
    Arguments:
        request {REQUEST} -- to specify the type of request
    
    Returns:
        JSONRESPONSE -- returns back the user_id
    """
    if request.is_ajax():
        user_id = request.POST.get('delete_id')
        return JsonResponse(delete_user_service(user_id, request.track_info))
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))




@logging_view
@login_required(login_url='usercp:login')
@premession(th_type1='manager',  role=['operational',])
def edit_user(request, user_id):
    """edit selected user by id
    
    Arguments:
        request {REQUEST} -- to specify methods
        id {INT} -- the user id
    
    Returns:
        RENDER -- rendres edit-user.html file if requested user has the required premession
    """
    user, user_form, roles, categories = edit_user_get_service(request.track_info, user_id)
    if request.method == "POST":
        form = request.POST
        file_value = request.FILES
        if edit_user_post_service(form, file_value, request.track_info, user) == True:
            return redirect('usercp:list_user')
        else:
            logger.error(str(edit_user_post_service(form, file_value, request.track_info, user)))
            messages.warning(request, str(edit_user_post_service(form, file_value, request.track_info, user)),
                             extra_tags='edit_user_form_error')
    return render(request, 'usercp/panel/edit-user.html', {'user_form': user_form, 'roles': roles, 'categories': categories})


@logging_view
@login_required(login_url='usercp:login')
# @user_tracker()
def add_to_mentor(request):
    """an ajax request to add the user as mentor to show him/her to mentors 
    
    Arguments:
        request {REQUEST} -- to specify method
    
    Returns:
        JSONRESPONSE -- returns back the user id
    """
    if request.is_ajax():
        acc_id = request.POST.get('add_id')
        return JsonResponse(add_to_mentor_service(request.track_info, acc_id))
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@logging_view
@login_required(login_url='usercp:register')
def send_sms_again(request):
    """allow user to try and resend verification code
    
    Arguments:
        request {REQUEST} -- to store and check sessions
    
    Returns:
        HTTPRESPONSE -- if the request is not ajax returns user to where they were
    """
    if request.is_ajax():
        send_sms_again_service(request.session)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@logging_view
@registerd_startup
def register_user(request):
    """the first stage for registring a startup if the requested use is not karmand
       if user submit his/her number, he/she will logout the system
    
    Arguments:
        request {REQUEST} -- to define is user is authenticated and store/check some values in session
    
    Returns:
        RENDER -- renders register.html file
    """
    
    form = UserRegisterForm()
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
        phone_form = request.POST
        form = UserRegisterForm(phone_form)
        service = register_user_condition_service(request.session, phone_form, form)
        if service == 'expired':
            messages.warning(request, 'لطفا بعدا تلاش کنید')
        elif service == 'karmand':
            messages.warning(request, f"این شماره قبلا در سیستم ثبت شده است، لطفاً به صفحه <a href='https://app.100startups.ir/login/'>ورود</a> مراجعه نمایید.", extra_tags='startup_validation')
            return redirect('usercp:register')
        elif service == 'success':

            return redirect('usercp:verify')
        elif service == 'exists':

            return redirect('usercp:verify')
        elif service == 'error':
            logger.error(str(form.errors))
            messages.warning(request, 'شماره موبایل اشتباه است')
    return render(request, 'usercp/site/register.html', {'form': form})


@logging_view
@registerd_startup
def verify_user(request):
    """in this stage user will enter the code that been sent to his/her phone number
       if there is no code and register_time in session he/she will reutrn to first stage
       
    
    Arguments:
        request {REQUEST} -- to define user and methods
    
    Returns:
        RENDER -- renders the verify.html file
    """
    if not 'sms_validate' in request.session or not 'register_timer' in request.session:
        return redirect('usercp:register')

    if request.method == 'POST':
        form = request.POST
        service = verify_user_service(request.session, form)
        if service[0] == 'loggedin':
            auth_login(request, service[1], backend='startups.backends.EmailBackend')
            if verify_user_track_user(request.session, request.track_info, service[1]):
                return HttpResponseRedirect('/{}/'.format(service[1].step))
            else:
                return redirect('usercp:dashboard_panel')
        if service == 'false':
            messages.warning(
                request, 'کدتایید اعتبارسنجی، اشتباه وارد شده است')
        if service == 'expired':
            messages.warning(request, 'کد اعتبار سنجی شما منقضی شد لطفا دوباره تلاش کنید')
    context = {'the_phone': request.session['phone'],
            'the_time': timezone.now().timestamp(),
            'register_time': parser.parse(request.session.get('register_timer')).timestamp() if request.session.get('register_timer') else None}
    return render(request, 'usercp/site/verify.html', context)




@logging_view
@login_required(login_url='usercp:register')
@registerd_startup
def startup(request):
    """allow user to fill information of his/her startup
    
    Arguments:
        request {REQUEST} -- to define user and method
    
    Returns:
        RENDER -- renders the startup.html file
    """
    if request.user.step in ['startup', 'team', 'upload', 'presentation', 'finish']:
        context = {'categories': Categories.objects.filter(is_available=True)}
        try:
            db_startup = fetch_startup_service(request.user, context)
            form_start = StartUpForm1(instance=db_startup)
            if request.method == 'POST':
                form = request.POST
                file_value = request.FILES
                form_start = StartUpForm1(
                    form, file_value, instance=db_startup)
                update_startup_service(form, file_value, request.user, request.track_info, form_start)
            context.update({"form_start": form_start})
        except StartUp.DoesNotExist:

            track_startup_creation_service(request.track_info)
            form_start = StartUpForm1()
            if request.method == 'POST':
                form = request.POST
                file_value = request.FILES
                form_start = StartUpForm1(form, file_value)
                startup_create_service(form, file_value, request.user, request.track_info, form_start)
            context.update({"form_start": form_start})
        finally:
            if request.method == 'POST':
                if assign_accelerator_or_leader(request.user, request.POST, form_start):
                    return redirect('usercp:team')
                else:
                    messages.warning(
                    request, 'شما نمیتوانید خود را بعنوان راهبر معرفی کنید')
                    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        return render(request, 'usercp/site/startup.html', context)
    else:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@logging_view
@login_required(login_url='usercp:register')
@registerd_startup
def team(request):
    """allow user to add team members to the his/her startup
    
    Arguments:
        request {REQUEST} -- to determine user and methods
    
    Returns:
        RENDER -- renders the team.html file
    """
    if request.user.step in ['team', 'upload', 'presentation', 'finish']:
        context = {}
        db_startup = team_instance_service(request.user, context, request.track_info)
        if request.method == "POST":
            form = request.POST
            file_value = request.FILES
            leader_form = LeaderUserForm(
                form, file_value, instance=request.user)
            userprofile_form = LeaderForm(
                form, instance=request.user.userprofile)
            form_start = StartUpForm5(form, instance=db_startup)
            if fill_team_info_service(form, file_value, leader_form, form_start, userprofile_form, request.user, request.track_info, db_startup):
                return redirect('usercp:upload')
            else:
                logger.error(
                    f"{leader_form.errors} {form_start.errors} {userprofile_form.errors}")
                messages.error(
                    request, f"{leader_form.errors} {form_start.errors} {userprofile_form.errors}")
        return render(request, 'usercp/site/team.html', context)
    else:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@logging_view
@login_required(login_url='usercp:register')
def remove_team_member(request):
    """remove selected team member by id
    
    Arguments:
        request {REQUEST} -- to define if request is ajax
    
    Returns:
        JSON -- returns the id that been deleted
    """
    if request.is_ajax():
        return JsonResponse(remove_team_member_service(request.POST))
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


# -----------[remove uploaded vidoe as ajax request]-----------------
# @logging_view
# @login_required(login_url='usercp:register')
# def remove_video(request):
#     if request.is_ajax():
#         the_id = request.POST.get('video_idss')
#         data = {
#             'video_idss': the_id,
#         }
#         st = get_object_or_404(StartUp, pk=the_id)
#         st.video = None
#         st.save()
#         return JsonResponse(data)
# --------------------------------------------------------------------


@logging_view
@login_required(login_url='usercp:register')
@registerd_startup
def upload(request):
    """a proxy page to upload video with out page freeze
    
    Arguments:
        request {REQUEST} -- to check user step and method
    
    Returns:
        RENDER -- renders upload.html file
    """
    if request.user.step in ['upload', 'presentation', 'finish']:
        if request.method == 'POST':
            return redirect('usercp:presentation')
        return render(request, 'usercp/site/upload.html')
    else:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required(login_url='usercp:register')
def upload_video_action(request):
    """the action page that the video actuly uploading
    
    Arguments:
        request {REQUEST} -- to specify requested user and method
    
    Returns:
        RENDER -- upload_video.html file
    """
    db_startup ,form = upload_video_service(request.user, request.track_info)
    if request.method == 'POST':
        form = StartUpForm2(request.POST, request.FILES, instance=db_startup)
        uploaded_video_service(form, request.track_info, db_startup)
    return render(request, 'usercp/site/upload_video.html', {'form': form})


@logging_view
@login_required(login_url='usercp:register')
@registerd_startup
def presentation(request):
    if request.user.step in ['presentation', 'finish']:
        startup_form, db_startup = presentation_service(request.user, request.track_info)
        if request.method == "POST":
            form = request.POST
            startup_form = StartUpForm3(
                form, request.FILES, instance=db_startup)
            if presentation_text_services(startup_form, form, request.session, request.track_info):
                return redirect('usercp:finish')
        return render(request, 'usercp/site/presentation.html', {'startup_form': startup_form})
    else:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))



def pgdeckxwlt(request, startup_id):
    """allow user to upload finance forecast with format of pdf
    
    Arguments:
        request {REQUEST} -- to determine method
        id {INT} -- the id of startup that we want to attach this file to it
    
    Returns:
        RENDER -- renders the page that the file actualy uploading
    """
    db_startup, startup_form = presentation_instance_file(startup_id, 'mali')
    if request.method == "POST":
        startup_form = StartUpForm6(
            request.POST, request.FILES, instance=db_startup)
        presentation_files_save(startup_form)
    return render(request, 'usercp/site/upload_xwlt.html', {'startup_e': startup_form})


def pgdeck(request, startup_id):
    """allow user to upload peachdeck file with format of pdf
    
    Arguments:
        request {REQUEST} -- to determine method
        id {INT} -- the id of startup that we want to attach this file to it
    
    Returns:
        RENDER -- renders the page that the file actualy uploading
    """
    db_startup, startup_form = presentation_instance_file(startup_id, 'pgdeck')
    if request.method == "POST":
        startup_form = StartUpForm4(
            request.POST, request.FILES, instance=db_startup)
        presentation_files_save(startup_form)
    return render(request, 'usercp/site/upload_pdf.html', {'startup_p': startup_form})


@logging_view
@login_required(login_url='usercp:register')
# @registerd_startup
def finish(request):
    """the last stage of registering startup
    
    Arguments:
        request {REQUEST} -- to define user session and status_of_user
    
    Returns:
        RENDER -- renders finish.html file
    """
    if request.user.step == 'finish':
        finish_service(request.user, request.session, request.track_info)
        if request.method == "POST":
            logout(request)
            return HttpResponseRedirect('http://100startups.ir/')
        return render(request, 'usercp/site/finish.html')
    else:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))



@logging_view
@login_required(login_url='usercp:login')
# @user_tracker()
def profile(request):
    context = {}
    if request.user.is_admin or request.user.user_type == 'manager':
        admin_form = admin_form_profile_service(request.user, request.track_info, context)
        if request.method == "POST":
            form = request.POST
            admin_form = admin_form_fill_service(request.user, form, request.track_info)
            if admin_form:
                return redirect('usercp:dashboard_panel')
            elif admin_form == "exists":
                messages.warning(request, 'adf', extra_tags='email_valid')
            elif admin_form == "failed":
                messages.warning(request, 'adf', extra_tags='smtw')

    else:
        role_form = role_form_profile_service(request.user, request.track_info, context)
        if request.method == "POST":
            form = request.POST
            file_value = request.FILES
            role_form = edit_role_profile_service(form, file_value, request.user, request.track_info)
            if role_form:
                return redirect('usercp:dashboard_panel')
            elif role_form == "exists":
                logger.error(str(role_form.errors))
                messages.warning(request, 'adf', extra_tags='email_valid')
            elif role_form == "failed":
                messages.warning(request, 'adf', extra_tags='smtw')

    return render(request, 'usercp/panel/profile.html', context)


@logging_view
@login_required(login_url='usercp:login')
def dashboard_panel(request):
    """the main page/dashboard panel that will show specific (objects/charts/etc) depends on user role
    
    Arguments:
        request {REQUEST} -- to define requested user and premessions
    
    Returns:
        RENDER -- returns contextes depend on user role
    """
    if request.user.user_type == 'startup' and request.user.step != 'finish':
        messages.warning(request, 'unfinished startup', extra_tags="cant_login_startup")
        return redirect('usercp:logout')
    context = {}
    default = dashboard_roles_service(request.user, context)

    if request.user.user_type == 'manager' or request.user.is_admin or request.user.can_see_startups == True or default[7] in request.user.role.all():
        context.update(dashboard_20_startups_services())

    if request.user.user_type == 'manager' or request.user.is_admin or default[7] in request.user.role.all():
        context.update(dashboard_chart_service(default[1] ,default[3] ,default[5] ,default[2] ,default[7], request.track_info))
        if request.is_ajax():
            the_year = request.GET.get('the_year')
            if the_year:
                return JsonResponse(list(dashboard_ajax_chart_service(the_year)), safe=False)

    if default[2] in request.user.role.all():
        search = {"s_startup1": request.GET.get('name_startup_referee1'),
                "s_startup2": request.GET.get('name_startup_referee2'),}
        context.update(dashboard_referee_service(request.track_info, request.user, search))

    if default[3] in request.user.role.all():
        dashboard_coach_service(request.track_info)
        context.update(dashboard_20_startups_services())

    if default[4] in request.user.role.all():
        context.update(dashboard_financial_service(request.track_info))

    if default[5] in request.user.role.all():
        context.update(dashboard_leader_service(request.track_info))

    if request.user.user_type == 'startup':
        context.update(dashboard_startup_service(request.user, request.track_info))

    if default[1] in request.user.role.all():
        invest_search = request.GET.get('name_startup_investor')
        the_id = request.GET.getlist('the_startup_id')
        context.update(dashboard_investor_service(request.user , invest_search, the_id, request.track_info, context))

    return render(request, 'usercp/panel/dashboard.html', context)


@logging_view
@login_required(login_url='usercp:login')
def profiles(request, user_id):
    """show some information of the selected user
    
    Arguments:
        request {REQUEST} -- to pass it to html file
        id {INT} -- to determine specific user
    
    Returns:
        RENDER -- renders selected user profile
    """
    
    return render(request, 'usercp/panel/profiles.html', get_user_service(id=user_id))


@logging_view
def login_view(request):
    """login view with 2 options:
       - login by phone number (sms verification code)
       - login by username/email and passowrd
       if requested user own a startup and didnot compelete the registartion cannot login
    
    Arguments:
        request {REQUEST} -- to check requested user status
    
    Returns:
        RENDER -- renders login html file
    """
    if request.user.is_authenticated:
        return redirect('usercp:dashboard_panel')

    form = LoginForm()
    if request.method == "POST":
        if request.POST.get('mobile'):

            if not validate_mobile_conditions_service(request.session):
                messages.warning(request, 'لطفا بعدا تلاش کنید',
                            extra_tags='can_login_phone')
            else:
                phone = request.POST.get('mobile')
                try:
                    the_user = get_user_service(phone=phone)
                    if the_user.user_type == 'startup' and the_user.step != 'finish':
                        messages.warning(request, 'unfinished startup', extra_tags="cant_login_startup")
                        return redirect('usercp:logout')
                    send_login_verification_service(the_user, request.track_info, request.session)
                    return redirect('usercp:verify_phone')
                except:
                    messages.warning(
                        request, 'چنین حسابی وجود ندارد', extra_tags='no_user_exists')

        else:
            form = LoginForm(request.POST)

            if form.is_valid():
                user = login_with_username_email_service(form, request.track_info)
                if user == 'exist':
                    messages.error(request, 'لطفاً با نام کاربری یا ایمیل وارد شوید', extra_tags='username_condition')
                    return redirect("usercp:login")
                else:
                    try:
                        auth_login(request, user,
                            backend='startups.backends.EmailBackend')
                    except Exception as e:
                        logger.error(str(e))
                        messages.warning(
                    request, 'نام کاربری یا کلمه عبور اشتباه می باشد', extra_tags='login_user_failed')
                    return redirect('usercp:dashboard_panel')

            else:
                messages.warning(
                    request, 'نام کاربری یا کلمه عبور اشتباه می باشد', extra_tags='login_user_failed')
                logger.error(str(form.errors))
                try:
                    status = f"کاربر  {request.POST.get('username')}نتوانست وارد حساب کاربری خود شود"
                    status_of_user(request, status, 'fail-login-dashboard')
                except:
                    pass
    return render(request, 'usercp/panel/login.html', {"form": form})


@logging_view
# @user_tracker()
def verify_phone(request):
    """if the time is not expired (deleted session) allow user to enter the sent code
    
    Arguments:
        request {REQUEST} -- to check session for code, timer and phone
    
    Returns:
        RENDER -- renders verify phone html file
    """
    try:
        expire_time = parser.parse(request.session['timer'])
    except:
        return redirect('usercp:login')
    if request.method == "POST":
        the_code = request.POST.get('the_code')
        success_login = login_verify_phone_service(the_code, expire_time, request.session, request.track_info)
        if success_login[0]== True:
            auth_login(request, success_login[1],
                        backend='startups.backends.EmailBackend')
            return redirect("usercp:dashboard_panel")

        elif login_verify_phone_service(the_code, expire_time, request.session, request.track_info)[0] == False: 
            messages.error(request, 'اشتباه است', extra_tags='the_code_is_not_valid')
        elif login_verify_phone_service(the_code, expire_time, request.session, request.track_info)[0] == 'expired':
            messages.warning(request ,'کد اعتبار سنجی شما منقضی شد لطفا دوباره تلاش کنید', extra_tags='svf')
            return redirect('usercp:login')
    return render(request, 'usercp/panel/verify_phone.html')
    

@logging_view
@login_required(login_url='usercp:login')
# @user_tracker()
def logout_view(request, *args, **kwargs):
    """logout the requested user
    
    Arguments:
        request {REQUSET} -- requested user
    
    Returns:
        HTTPRESPONCE -- reidrect user to login page
    """
    logout(request, *args, **kwargs)
    return redirect('usercp:login')


@logging_view
# @user_tracker()
def profile_mentor(request):
    """list of coaches and leaders that added as mentors
    
    Arguments:
        request {REQUEST} -- to pass it as context to html file
    
    Returns:
        RENDER -- renders the profile mentor html file
    """
    search = {
        "full_search": request.GET.get('full_search') ,
        "cats": request.GET.get('cats'),
    }
    return render(request, 'usercp/panel/profile-mentor.html', profile_mentor_service(search))


@logging_view
@premession(th_type1='manager', role=['operational', ])
# @user_tracker()
def sort_mentors(request):
    """allow admins to sort the mentors by moving their pictures
    
    Arguments:
        request {REQUEST} -- to pass as e context to html file
    
    Returns:
        RENDER -- renders the users that has been chosen as mentors order_by the sort number
    """
    the_mentors = sort_mentors_service()
    if request.method == "POST":
        user_sort_num = request.POST
        if sort_mentors_sort_service(the_mentors, user_sort_num, request.track_info):
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            messages.warning(request ,'مشکلی پیش آمده. دوباره تلاش کنید', extra_tags='sorting_error')
    return render(request, 'usercp/panel/sort-mentors.html', {'the_mentors': the_mentors})



def my_404_error(request, *args, **kwargs):
    """custom 404 html
    
    Arguments:
        request {REQUEST} -- to pass to tempalte as context
    
    Returns:
        RENDER -- renders 404.html if 404 happens
    """
    return render(request, '404.html')



def my_500_error(request, *args, **kwargs):
    """custom 500 html
    
    Arguments:
        request {REQUEST} -- to pass as context to template
    
    Returns:
        RENDER -- renders 500.html file
    """
    return render(request, '500.html')


@login_required(login_url='usercp:login')
def ghost_mode(request, user_id):
    if request.user.is_admin:
        user = get_user_service(pk=user_id)
        user_id = request.user.id
        update_session_auth_hash(request, user)
        auth_login(request, user, backend='startups.backends.EmailBackend')
        if user.user_type == 'startup' and user.step != 'finish':
            request.session['iam_ghosting'] = user_id
            return HttpResponseRedirect(f'/{user.step}/')
        request.session['iam_ghosting'] = user_id
        return redirect('usercp:dashboard_panel')
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))



@login_required(login_url='usercp:login')
def ghost_mode_out(request):
    if 'iam_ghosting' in request.session:
        user = get_user_service(pk=int(request.session.get('iam_ghosting')))
        auth_login(request, user, backend='startups.backends.EmailBackend')
        return redirect('usercp:dashboard_panel')
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))





# @logging_view
# def checkout_leader(request):
#     role = models.Role.objects.get(name='leader')
#     leaders = models.User.objects.filter(role=role, mentor_user=True)
#     return render(request, 'panle/checkout-leader.html', {'leaders': leaders})

# @login_required(login_url='usercp:register')
# def check_email(request):
#     if request.is_ajax():
#         th_email = request.POST.get('email')
#         if models.User.objects.filter(email__iexact=th_email).exists():
#             return False
#         return True


# @logging_view
# @login_required(login_url='usercp:register')
# # @user_tracker()
# def accept_as_leader(request):
#     if request.is_ajax():
#         leader_id = request.POST.get('leader_id')
#         leader = get_user_service(id=int(leader_id))
#         leader.mentor_user = False
#         leader.save()
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
