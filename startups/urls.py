"""kaweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.conf import settings
from usercp import views
from .api import shetabs_json, startups_api

urlpatterns = [
     path('', views.redirect_url_to_register, name='redirect_url'),
     path('admin/', admin.site.urls),
     path('admin/doc/', include('django.contrib.admindocs.urls')),
     path('', include(('usercp.urls', 'usercp'), namespace='usercp')),
     path('', include(('startup.urls', 'startup'), namespace='startup')),
     path('', include(('theevent.urls', 'theevent'), namespace='theevent')),
     path('', include(('category.urls', 'category'), namespace='category')),
     path('', include(('usertracker.urls', 'usertracker'), namespace='usertracker')),
     path('', include(('message.urls', 'message'), namespace='message')),

     path('api/', shetabs_json, name='shetabs_json'),
     path('api/startup/', startups_api, name='shetabs_json'),
     path('logs/all', views.all_logs, name='my_logs'),
     path('logs/urls', views.url_logs, name='url_logs'),
]

handler404 = views.my_404_error
handler500 = views.my_500_error

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
