from django.shortcuts import render
from .services import *
from django.contrib.auth.decorators import login_required


@logging_view
@login_required(login_url='usercp:login')
def user_activities(request):
    """[render to show user activities in different conditions]"""
    return render(request, 'usertracker/user-activities.html', context=activity_search(request))

