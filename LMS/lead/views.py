from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import transaction

# local imports
from LMS.lead.models import Lead, DocumentType, Document
from LMS.address.models import City, UserAddress


class LeadView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data

        required_fields = ['mobile', 'name',  'age', 'occupation', 'income', 'city',
                           'source', 'address', 'pincode']
        missing_fields = set(required_fields) - set(data.keys())
        if missing_fields:
            resp = {
                "message": "%s Fields are required" % (list(missing_fields))
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=resp)
        city = City.objects.filter(name=data.get('city')).first()
        doc_names = dict(DocumentType.objects.values_list('name', 'id'))
        if Lead.objects.filter(phone_number=data.get('mobile')).exists():
            resp = {
                "message": "Lead For this mobile number exists"
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=resp)

        with transaction.atomic():
            address = UserAddress.objects.create(line1=data.get('address'), city_id=city.id)
            lead = Lead.objects.create(
                phone_number=data.get('mobile'),
                age=data.get('age'),
                name=data.get('name'),
                occupation=data.get('occupation'),
                income=data.get('income'),
                source=data.get('source'),
                city_id=city.id,
                address=address)
            for key, val in doc_names.items():
                # key will be doc type like aadhar pan and val will be its DB id
                # generic way to capture document and its number
                if key in data.keys():
                    Document.objects.create(lead=lead, number=data.get(key+'_number'), file=data.get(key),
                                            document_type_id=val)
        resp = {
            "message": "Lead Created"
        }
        return Response(status=status.HTTP_200_OK, data=resp)
