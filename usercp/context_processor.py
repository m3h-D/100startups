from .dashboard_services import get_role_service


def is_oprational(request):
    """a context processor to check the requested user role
    
    Arguments:
        request {REQUEST} -- to pass as context to template
    
    Returns:
        DICT -- returns objects of role model
    """
    return {'is_op': get_role_service(name='operational'),
    'is_leader': get_role_service(name='leader'),
    'is_finance': get_role_service(name='financial'),
    'is_investor': get_role_service(name='investor'),}

