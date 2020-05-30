from .utils import get_client_ip
from django.utils.deprecation import MiddlewareMixin
from django.contrib.contenttypes.models import ContentType
from django_user_agents.utils import get_user_agent
from django.contrib.sites.shortcuts import get_current_site
from usertracker.models import UserTracker
from startups.utils import get_client_ip
from urllib.parse import urlsplit
from startups.object import get_user_service
from startup.models import StartUp
import re
from django.urls import resolve


class UserStatusMiddleware:
    """this middleware gets user ip and id for adding status to user action(UserTracker)
    """    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_id = request.user.id
        user_ip = get_client_ip(request)
        request.track_info = { 'user_id': user_id, 'user_ip': user_ip}
        response = self.get_response(request)
        return response


class UserTrackerMiddleware:
    """this middleware track users actions at every link except admin panel
       and when admin goes to ghost mode
       to assign instance to UserTracker will resolve url and then get kwargs of function for that url
       then split the key in the first index there is the model of object for content type and for the id of object
       will use value of the kwargs.
    """    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if '/admin/' not in request.path and not 'iam_ghosting' in request.session:
            match = resolve(str(request.path))
            model = None
            id = None
            instance = None
            if '_id' in str(match.kwargs):
                for key, val in match.kwargs.items():
                    model = str(str(key).split('_')[0])
                    id = val
                model_qs = ContentType.objects.get(model=model)
                Model = model_qs.model_class()
                instance = Model.objects.get(id=id)
            # -----------------------------------------------------
            protocol = urlsplit(request.build_absolute_uri(None)).scheme
            current_site = get_current_site(request)
            current_path = request.path
            url = ''.join(
                [str(protocol), '://', str(current_site), str(current_path)])
            # -----------------------------------------------------
            if request.user.is_authenticated:
                UserTracker.objects.create_by_model(
                    user=request.user,
                    url=url,
                    instance=instance,
                    user_agent=str(get_user_agent(request)),
                    user_ip=get_client_ip(request)
                )
            else:
                try:
                    th_user = get_user_service(phone=request.session['phone'])
                except:
                    th_user = None
                UserTracker.objects.create_by_model(
                    user=th_user,
                    url=url,
                    instance=instance,
                    user_agent=str(get_user_agent(request)),
                    user_ip=get_client_ip(request)
                )
        response = self.get_response(request)
        return response