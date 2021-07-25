from rest_framework import status, generics, views
from django.conf import settings
import json
import requests
from rest_framework.response import Response


url = 'https://twilix.exotel.in/v1/Accounts/%s/Sms/send.json' % settings.EXOTEL_API_SID


class CallMasking(generics.RetrieveAPIView):
    def post(self, request):
        data = request.data
        customer_number = data.get('customer_number')
        user = request.user
        url = settings.EXOTEL_MASKING % (settings.EXOTEL_API_KEY, settings.EXOTEL_API_TOKEN, settings.EXOTEL_API_SID)
        data = {
            'From': str(user.phone_number),
            'To': customer_number,
            'CallerId': 'XXXXXXX',
            "StatusCallback": settings.HOST_URL+ '/api/exotel/call/update',
            "StatusCallbackEvent": "terminal",
            "StatusCallbackContentType": "application/json"
        }
        res = requests.post(url, data=data)
        data = json.loads(res.content)
        response = {
            "message": "Failed to make a call"
        }
        if res.status_code == status.HTTP_200_OK:
            response = {
                "message": "you will get a callback soon"
            }
            return Response(status=status.HTTP_200_OK, data=response)
        resp = {
            "message": "failed to make a call"
        }
        return Response(status=status.HTTP_400_BAD_REQUEST, data=resp)


def send_message(sms_from, sms_to, message, template_dict, priority=''):

    parm = {
            'From': sms_from,
            'To': sms_to,
            'Body': message,
            'Priority': priority,
            'DltEntityId': settings.DLT_ENTITY_ID,
            'StatusCallback': settings.SMS_CALLBACK_URL
        }

    tid = template_dict.get('template_id', None)
    if tid:
        parm['DltTemplateId'] = tid

    response = requests.post(url.format(sid=settings.EXOTEL_API_SID, status_call_back=settings.SMS_CALLBACK_URL),
                             auth=(settings.EXOTEL_API_SID, settings.EXOTEL_API_TOKEN), data=parm)

    return response
