from django.urls import path, include
from startup import views
from startups.utils import export_list_csv

urlpatterns = [
     path('popups/<int:requests_id>/', views.pop_up, name='pop_up'),
     path('list-startup/', views.list_startup, name='list_startup'),
     path('list-referee/', views.list_referee, name='list_referee'),
     path('list-investor/', views.list_investor, name='list_investor'),
     path('investor-can-see/', views.investor_can_see, name='investor_can_see'),
     path('add-for-invest/', views.add_for_invest, name='add_for_invest'),
     path('list-coach/', views.list_coach, name='list_coach'),
     path('list-accelerator/', views.list_accelerator, name='list_accelerator'),
     path('delete-accelerator/', views.delete_accelerator,
          name='delete_accelerator'),
     path('edit-startup/<int:startup_id>/', views.edit_startup, name='edit_startup'),
     path('information-startup/<int:startup_id>/', views.information_startup, name='information_startup'),
     path('delete-startup/', views.delete_startup, name='delete_startup'),
     path('delete-referee/', views.remove_referee_form_startup, name='remove_referee_form_startup'),
     path('select-startup/', views.select_startup, name='select_startup'),
     path('my-startup/', views.my_startup_information, name='my_startup_information'),
     path('score-again/', views.can_score_again, name='can_score_again'),

     path('edit-accelerator/<int:shetabdahande_id>/',
          views.edit_accelerator, name='edit_accelerator'),

     path('create-accelerator/', views.create_accelerator,
          name='create_accelerator'),
     path('information/<int:startup_id>/', views.information, name='information'),
     path('reconsider/', views.reconsider, name='reconsider'),
     path('information-accelerator/<int:id>/', views.information_accelerator,
          name='information_accelerator'),
     path('manage-request/', views.manage_request, name='manage_request'),
     path('request-money/', views.request_money, name='request_money'),
     path('send-request-money/', views.send_request_money, name='send_request_money'),
     path('madrak-doc/<int:startup_id>/', views.verify_startup_documents, name='verify_startup_documents'),
     path('startup-doc/<int:startup_id>/', views.startup_assessment, name='startup_assessment'),
     path('modir-doc/<int:startup_id>/', views.verify_not_presence_referee, name='verify_not_presence_referee'),
     path('suspend/<int:startup_id>/', views.suspend_startup, name='suspend_startup'),
     path('pres-doc/<int:startup_id>/', views.verify_presence_referee, name='verify_presence_referee'),
     path('single-requestmoney/<int:requests_id>/', views.single_requestmoney, name='single_requestmoney'),
     path('export/xls/<the_model>/', export_list_csv, name='export_list_csv'),
     path('add-to-investor/<int:startup_id>/', views.add_to_investor, name='add_to_investor'),
]