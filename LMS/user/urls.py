from django.conf.urls import url
from django.apps import AppConfig
from LMS.user.views import Login
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^user/login',  Login.as_view(), name='login-api'),
]

