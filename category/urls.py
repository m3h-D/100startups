from django.urls import path, include
from category import views

urlpatterns = [
    
     path('list-cat/', views.list_cat, name='list_cat'),
     path('can-see-cat/', views.can_see_cat, name='can_see_cat'),
     path('edit-cat/<int:categories_id>/<slug>/', views.edit_cat, name='edit_cat'),
     path('delete-cat/', views.delete_cat, name='delete_cat'),
     path('create-cat/', views.create_cat, name='create_cat'),
]