from django.urls import path, include
from usertracker import views

urlpatterns = [
     path('user-activities/', views.user_activities, name='user_activities'),
]