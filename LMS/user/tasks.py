from celery import Celery

from LMS.common.exotel import send_message

app = Celery()
from LMS import celery_app
from django.conf import settings


@celery_app.task(max_retries=settings.CELERY_EVENT_MAX_RETRIES, ignore_result=False)
def send_sms(sms_from, sms_to, message, template_dict):
    send_message(sms_from, sms_to, message, template_dict)