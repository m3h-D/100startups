from usercp import models
from startups.object import get_role_service
from startup.models import StartUp, ShetabDahande, Investors
from django.http import JsonResponse
from .utils import logging_view
import operator
from functools import reduce
from django.db.models import Q
from django.forms.models import model_to_dict
from django.contrib.sites.shortcuts import get_current_site
from urllib.parse import urlsplit
from persiantools.jdatetime import JalaliDateTime
from django.db.models import F
import datetime





@logging_view
def shetabs_json(request):
    result = []
    try:
        fields = request.GET.get('fields').split()
    except:
        fields = request.GET.get('fields')
    
    th_fields = request.GET.get('fields')

    investor = request.GET.get('investorId')
    try:
        the_search = reduce(operator.__and__, [Q(first_name__icontains=query) | Q(
            last_name__icontains=query) for query in fields])
    except:
        pass
    if investor:
        database = StartUp.objects.filter(
            investor__user__pk=int(investor))
        for db in database:
            result.append({
                'startup_name': db.title,
                'startup_id': db.pk,
            })
    if fields:
        if request.GET.get('type') == 'leader':
            role = get_role_service(name='leader')

            database = role.user.filter(mentor_user=False).filter(the_search)
            for db in database:
                result.append({
                    'id': db.pk,
                    'name': db.first_name + ' ' + db.last_name
                })
        elif request.GET.get('type') == 'accelerator':
            database = ShetabDahande.objects.filter(name_namayande__mentor_user=False).filter(name_shtabdahande__icontains=th_fields
                                                    )
            for db in database:
                result.append({
                    'id': db.pk,
                    'name': ' '.join([db.name_shtabdahande])
                })
        elif request.GET.get('type') == 'managers':
            role = get_role_service(name='leader')
            database = models.User.objects.filter(role=role).filter(the_search)
            for db in database:
                result.append({
                    'id': db.pk,
                    'name': db.first_name + ' ' + db.last_name
                })
        if request.GET.get('type') == 'referee':

            role = get_role_service(name='referee')

            database = role.user.filter(the_search)

            for db in database:
                result.append({
                    'id': db.pk,
                    'name': db.first_name + ' ' + db.last_name
                })

        if request.GET.get('type') == 'coach':

            role = get_role_service(name='coach')

            database = role.user.filter(the_search)

            for db in database:
                result.append({
                    'id': db.pk,
                    'name': db.first_name + ' ' + db.last_name
                })

        if request.GET.get('type') == 'subscriber':
            database = StartUp.objects.filter(title__icontains=th_fields,)

            if request.GET.get('companion') == 'companion':

                database = StartUp.objects.filter(
                    shetab_dahande__isnull=True, rahbar_asli__isnull=True).filter(title__icontains=th_fields)

            for db in database:
                result.append({
                    'id': db.pk,
                    'name': db.title
                })

        if request.GET.get('type') == 'investor':
            role = get_role_service(name='investor')

            database = role.user.filter(the_search)
            for db in database:
                result.append({
                    'id': db.pk,
                    'name': db.first_name + ' ' + db.last_name
                })

        if request.GET.get('type') == 'users':

            database = models.User.objects.filter(the_search)
            for db in database:
                result.append({
                    'id': db.pk,
                    'name': db.first_name + ' ' + db.last_name
                })

    return JsonResponse(result, safe=False)


def startups_api(request):
    """an api to show startups that have credit in 100startups main page

    Arguments:
        request {REQUEST} -- for HTTP Response

    Returns:
        JSONRESPONSE -- returns serialized informaion about startup
    """    
    protocol = urlsplit(request.build_absolute_uri(None)).scheme
    current_site = get_current_site(request)
    result = []
    startup = StartUp.objects.filter(credit__isnull=False)
    site = ''.join([str(protocol),'://',str(current_site)])
    for db in startup:
        date = JalaliDateTime.to_jalali(datetime.datetime(db.created_date.year, db.created_date.month, db.created_date.day, db.created_date.hour, db.created_date.minute, db.created_date.second, 0))
        result.append({
            'id': db.id,
            'logo': site + str(db.image.url),
            'name': db.title,
            'site': db.site,
            'credit': db.credit,
            'explaine': db.explain_startup,
            'created_date': str(date),
            'leader': {'first_name': db.rahbar_asli.first_name, 'last_name': db.rahbar_asli.last_name, 'avatar': site + str(db.rahbar_asli.avatar.url)},
            'investor':  list(db.investor.annotate(avatar=F('user__avatar'), first_name=F('user__first_name'), last_name=F('user__last_name')).values('avatar', 'first_name', 'last_name')),
            'team': list(db.teammember.annotate(first_name=F('t_first_name'), last_name=F('t_last_name'), avatar=F('t_avatar'), role=F('t_role_in_startup')).values('first_name', 'last_name', 'avatar', 'role'))

        })
    return JsonResponse(result, safe=False)