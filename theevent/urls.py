from django.urls import path, include
from . import views


urlpatterns = [
    path('offerto-leader/', views.offerto_leader, name='offerto_leader'),
    path('list-offer/', views.list_offer, name='list_offer'),
    path('list-meeting/', views.list_meeting, name='list_meeting'),
    path('edit-meeting/<int:theevent_id>/', views.edit_meeting_coach, name='edit_meeting_coach'),
    path('edit-offer/<int:theevent_id>/', views.edit_offer_to_leader, name='edit_offer_to_leader'),
    path('edit-event/<int:theevent_id>/', views.edit_create_event, name='edit_create_event'),
    path('wants-meet/', views.wants_to_meet, name='wants_to_meet'),
    path('list-event/', views.list_event, name='list_event'),
    path('meeting-coach/', views.meeting_coach, name='meeting_coach'),
    path('create-event/', views.create_event, name='create_event'),
    path('add-to-leader/', views.add_to_leader, name='add_to_leader'),
]