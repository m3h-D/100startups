from django.urls import path, include
from message import views

urlpatterns = [
     path('send-message/chat/<int:user_id>/',
          views.send_message_chat, name='send_message_chat'),
     path('send-message/error/',
          views.send_message_error, name='send_message_error'),
     path('box-message/',
          views.message_box, name='message_box'),
     path('notification/', views.notification, name='notification'),
     path('show-messages/<int:allmessages_id>/', views.show_messages, name='show_messages'),
     path('support/', views.support_msg, name='support_msg'),
]