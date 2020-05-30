from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core import files
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from . import models
from usertracker.models import UserTracker
from django.core.paginator import Paginator
from .forms import CategoryForm

from django.contrib.auth.decorators import login_required
from startups.utils import get_client_ip, premession, logging_view, status_of_user, resize_pics
from .services import *
import re
import logging

logger = logging.getLogger(__name__)

# Create your views here.


@logging_view
@login_required(login_url='usercp:login')
@premession(th_type1='manager',  role=['operational', ])
# @user_tracker()
def list_cat(request):
    """list of categories with pagination

    Arguments:
        request {REQUEST} -- to get page number and track user

    Returns:
        RENDER -- renders the list-cat html file
    """    
    offset = request.GET.get('page')
    return render(request, 'category/list-cat.html', list_category_service(request.track_info, offset))


@logging_view
@login_required(login_url='usercp:login')
# @user_tracker()
def delete_cat(request):
    """allow user to delete specific category which id of it will given by ajax

    Arguments:
        request {REQUEST} -- to check if the reqeust is ajax

    Returns:
        JSONRESPONSE -- returns back the id of the category to ajax
    """    
    if request.is_ajax():
        cat_id = request.POST.get('delete_cat_id')
        return JsonResponse(delete_category_service(cat_id, request.track_info))
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@logging_view
@login_required(login_url='usercp:login')
@premession(th_type1='manager',  role=['operational', ])
# @user_tracker(model='categories')
def create_cat(request):
    """allow users with role of admin or manager or operational to create a new category

    Arguments:
        request {REQEUST} -- to define method of form and get image

    Returns:
        RENDRES -- renders the create-cat html file
    """    
    if request.method == "POST":
        file_value = request.FILES
        form = request.POST
        cat_form = create_category_service(form, file_value, request.track_info)
        if cat_form == True:
            return redirect('category:list_cat')
        else:
            messages.warning(request, str(cat_form),
                             extra_tags='category_error')

    return render(request, 'category/create-cat.html')


@logging_view
@login_required(login_url='usercp:login')
@premession(th_type1='manager',  role=['operational', ])
# @user_tracker(model='categories')
def edit_cat(request, categories_id, slug):
    """allow users with role of admin or manager or operational to edit specific category

    Arguments:
        request {REQUEST} -- to 
        id {INT} -- the id of selected category
        slug {SLUG} -- the slug of selected category

    Returns:
        RENDRES -- renders the edit-cat html file
    """    
    cat_form, category =  edit_category_instance_service(categories_id, slug)
    if request.method == "POST":
        file_value = request.FILES
        form = request.POST
        cat_form = edit_category_service(form, file_value, request.track_info, category)
        if cat_form == True:
            return redirect('category:list_cat')
        else:
            messages.warning(request, str(cat_form),
                             extra_tags='edit_cat_form_error')
    return render(request, 'category/edit-cat.html', {"cat_form": cat_form,"category": category})


@logging_view
@login_required(login_url='usercp:login')
# @user_tracker()
def can_see_cat(request):
    """give selection access to category on registeration process or vice versa

    Arguments:
        request {REQUEST} -- to check if the request is ajax or not

    Returns:
        JSONRESPONSE -- returns back the id of the category to ajax
    """    
    if request.is_ajax():
        cat_id = request.POST.get('add_id')
        return JsonResponse(can_see_category_service(cat_id))
    return HttpResponseRedirect(request.META.get("HTTP_REFEREE"))
