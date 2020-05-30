from django.shortcuts import get_object_or_404
from startup.models import StartUp
from usercp.models import User, Role
from theevent.models import CreateEvent

def get_startup_service(**kwargs):  
    """get the startup with specified keywordargument

    Returns:
        OBJECT -- returns the chosen startup
    """
    return get_object_or_404(StartUp, **kwargs)


def get_role_service(**kwargs):
    """get the role with specified keywordargument

    Returns:
        OBJECT -- returns the chosen role
    """
    return get_object_or_404(Role, **kwargs)


def get_user_service(**kwargs):
    """get the user with specified keywordargument

    Returns:
        OBJECT -- returns the chosen user
    """
    return get_object_or_404(User, **kwargs)



def get_create_event_service(**kwargs):
    """get the createevent with specified keywordargument

    Returns:
        OBJECT -- returns the chosen user
    """
    return get_object_or_404(CreateEvent, **kwargs)