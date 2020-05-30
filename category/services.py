from django.shortcuts import get_object_or_404
from django.core import files
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CategoryForm
from startups.utils import *
from . import models
import logging

logger = logging.getLogger(__name__)


def list_category_service(track_info, offset):
    """list of all categories

    Arguments:
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        DICT -- returns dictionary of categories queryset
    """    
    status = "لیست دسته ها را دید"
    status_of_user(track_info, status, 'import-list-cat')
    categories = models.Categories.objects.all().order_by('-created_date')
    paginator = Paginator(categories, 30)
    page = offset
    categories = paginator.get_page(page)
    return {'categories': categories}    


def delete_category_service(cat_id, track_info):
    """delete the selected category by the given id

    Arguments:
        cat_id {INT} -- id of the category
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        DICT -- returns dictionary that includes category id
    """    
    data = {
        'delete_cat_id': cat_id
    }
    the_cat = get_object_or_404(models.Categories, id=cat_id)
    status = f"دسته {the_cat.title} را حذف کرد"
    status_of_user(track_info, status, 'import-list-cat')
    the_cat.delete()
    return data


def create_category_service(form, file_value, track_info):
    """create new category using CategoryForm it will resize the image but it's not base-64

    Arguments:
        form {POST Method} -- to define form method
        file_value {FILES Method} -- to get image file
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        BOOLEAN/STRING -- returns True if form is valid else returns forms errors
    """    
    cat_form = CategoryForm(form)
    if cat_form.is_valid():
        try:
            image_b64 = file_value.get('image')
            th_img , ext = resize_pics(image_b64)
            cat_form.instance.image.save(f'category.{ext}', files.File(th_img), save=False)
        except:
            pass
        cat_form.save()
        status = f"دسته {cat_form.instance.title} را ساخت"
        status_of_user(track_info, status, 'import-create-cat')
        return True
    else:
        logger.error(str(cat_form.errors))
        return cat_form.errors


def edit_category_instance_service(pk, slug):
    """get category that selected to edit by pk and slug

    Arguments:
        pk {PRIMARY KEY/INT} -- a unique field to get selected category
        slug {SLUG} -- get category object with slug(plus pk)

    Returns:
        FORM -- returns category form instance
    """    
    category = get_object_or_404(models.Categories, pk=pk, slug=slug)
    cat_form = CategoryForm(instance=category)
    return cat_form, category


def edit_category_service(form, file_value, track_info, category):
    """edit current category object with Form Model of Categories

    Arguments:
        form {POST Method} -- to define CategoryForm method
        file_value {FILES Method} -- to get image for category
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        BOOLEAN/STRING -- returns True if form is valid else returns forms errors
    """    
    cat_form = CategoryForm(form, instance=category)
    if cat_form.is_valid():
        try:
            image_b64 = file_value.get('image')
            th_img , ext = resize_pics(image_b64)
            cat_form.instance.image.save(f'category.{ext}', files.File(th_img), save=False)
        except:
            pass
        cat_form.save()
        status = f"مشخصات دسته {cat_form.instance.title} را تغییر داد"
        status_of_user(track_info, status, 'import-edit-cat')
        return True
    else:
        logger.error(str(cat_form.errors))
        return cat_form.errors


def can_see_category_service(cat_id):
    """with an ajax request the selected category will be available in registeration process and can be select by owner of startup
       if the category is already available after click it become unavailable and vice versa 

    Arguments:
        cat_id {INT} -- the category id that will get specific category object

    Returns:
        DICT -- returns back a dictionary of categorys id
    """    
    data = {
        'add_id': cat_id,
    }
    cat = models.Categories.objects.get(pk=cat_id)
    if cat.is_available == False:
        cat.is_available = True
        cat.save()
    else:
        cat.is_available = False
        cat.save()
    return data