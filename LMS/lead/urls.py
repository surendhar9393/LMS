from django.conf.urls import url
from django.apps import AppConfig
from LMS.lead.views import LeadView

urlpatterns = [
    url(r'^lead', LeadView.as_view(), name='lead'),
]

