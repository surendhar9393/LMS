from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from LMS.user.views import index
from django.conf.urls.static import static
from django.config import settings


# local imports
from LMS.user import views

urlpatterns = [
    url(r'', index, name='index'),


    # url(r'', views.index, name='index'),
    url(r'^api/', include('LMS.urls')),
]
