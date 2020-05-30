from usertracker import models
from startups.utils import *
from persiantools.jdatetime import JalaliDate, JalaliDateTime
from django.utils import timezone
from django.core.paginator import Paginator



def activity_search(request):
    """[user activities]
    
    Arguments:
        request {[request]} -- [get values to search in side the UserTracker Model]
    
    Returns:
        [DICT] -- [return result of the qs/pagination/category]
    """
    if request.user.user_type == 'manager':
        trackers = models.UserTracker.objects.filter(user__is_admin=False)
    elif request.user.is_admin == True:
        trackers = models.UserTracker.objects.all()
    else:
        trackers = models.UserTracker.objects.filter(user=request.user)
    the_trackers = None
    start_up = request.GET.get('startup_id')
    user_id = request.GET.get('user_id')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    category = request.GET.getlist('body[]')
    the_statuses = models.TheStatus.objects.all()

    if start_up:
        trackers = trackers.filter(object_id=start_up)
    if user_id:
        trackers = trackers.filter(user__pk=user_id)

    if start_date and end_date:
        end_date_lists = get_list(end_date)
        e_date = JalaliDate(
            end_date_lists[0], end_date_lists[1], end_date_lists[2]).to_gregorian()
        start_date_lists = get_list(start_date)
        s_date = JalaliDate(
            start_date_lists[0], start_date_lists[1], start_date_lists[2]).to_gregorian()
        new_end = e_date + timezone.timedelta(days=1)
        trackers = trackers.filter(created_date__range=[s_date, new_end])

    if category:
        trackers = trackers.filter(the_status__name__in=category)

    paginator = Paginator(trackers, 30)
    page = request.GET.get('page')
    trackers = paginator.get_page(page)
    return {'trackers': trackers, "the_trackers": the_trackers, 'page': page, "the_statuses": the_statuses,
                                                          'start_up': start_up,
                                                          'user_id': user_id,
                                                          'start_date': start_date,
                                                          'end_date': end_date,
                                                          'category': category, }