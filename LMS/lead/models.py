from datetime import date
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django_fsm import FSMField, transition

from LMS.user.models import LeadUser
from .transition_conditions import is_sales_user

FRESH = 'Fresh'
FORM_PENDING = 'Form Pending'
PENDING = 'Document Pending'
HOT_APPLICATION = 'Hot Application'
APPROVED = 'Approved'
REJECTED = 'Rejected'
CONVERTED = 'Converted'
CLOSED = 'Closed'

LEAD_STATUS_CHOICES = (
    (FRESH, 'Fresh'),
    (FORM_PENDING, 'Form Pending'),
    (PENDING, 'Document Pending'),
    (HOT_APPLICATION, 'TIER_3'),
    (APPROVED, 'TIER_3'),
    (REJECTED, 'TIER_3'),
    (CONVERTED, 'TIER_3'),
    (CLOSED, 'TIER_3'),
)

FB = 'Fb'
WEB = 'WebSite'
GOOGLE = 'Google'


SOURCES = (
   (FB, 'Fb'),
   (WEB, 'WebSite'),
   (GOOGLE, 'Google'),
)
MEDIA_UPLOAD_STRUCTURE = getattr(settings, "MEDIA_UPLOAD_STRUCTURE", "")


def generate_file_path(instance, filename):
    """
    Returns the file path as per the defined directory structure.
    """

    doc_code = instance.document_type.name.replace(" ", "_")
    module_name = instance._meta.app_label + "s"
    instance_label = instance._meta.object_name.lower().replace("document", "")
    if hasattr(instance, instance_label+"_id"):
        instance_handle = instance_label + "_" + str(getattr(instance, instance_label+"_id"))
    else:
        instance_handle = instance_label + "_" + str(instance.id)

    file_name = str(date.today()) + "/" + "/" + filename.upper()

    return MEDIA_UPLOAD_STRUCTURE.format(
        module_name=module_name,
        instance_handle=instance_handle,
        doc_code=doc_code,
        file_name=file_name
    ).replace("//", "/")


class Occupation(models.Model):
    name = models.CharField(_('Name'), max_length=255, unique=True)

    is_active = models.BooleanField(_('Is Active'), default=True)


class DocumentType(models.Model):
    name = models.CharField(_("Document Type"), max_length=64, unique=True,
        help_text=_("Document name like Aadhar, PAN, Licence, etc.."),
    )

    creation_date = models.DateTimeField(_("Creation Date"), auto_now_add=True)

    def __str__(self):
        return self.name


class Document(models.Model):
    file = models.FileField(
        upload_to=generate_file_path, max_length=256
    )
    document_type = models.ForeignKey(
        DocumentType,
        on_delete=models.PROTECT,
        help_text=_("Document type like Registration Certificate, Licence, etc.."),
    )

    number = models.CharField(
        _("Document Number"),
        max_length=100,
        default="----",
        help_text=_("Input the number from the file uploaded.."),
    )
    lead = models.ForeignKey('lead.Lead', on_delete=models.PROTECT)


class Lead(models.Model):
    name = models.CharField(
        _('Name of User'), max_length=255)

    phone_number = PhoneNumberField(
        _("Mobile Number"), blank=True, unique=True,
        help_text=_("Customer's primary mobile number e.g. +91{10 digit mobile number}"))

    # status = models.CharField(_('Status'), max_length=60, choices=LEAD_STATUS_CHOICES, default=FRESH)
    status = FSMField(default=FRESH, protected=False, db_index=True)

    age = models.PositiveIntegerField(_('Age'), null=True, blank=True)

    occupation = models.CharField(_('Status'), max_length=60, null=True, blank=True)

    income = models.DecimalField(_("Monthly Income"), max_digits=10, decimal_places=2, default=0)

    city = models.ForeignKey('address.City', on_delete=models.PROTECT)

    address = models.ForeignKey('address.UserAddress',  on_delete=models.PROTECT)

    action_owner = models.ForeignKey('user.User', on_delete=models.PROTECT, null=True, blank=True,
                                     related_name='action_owner')

    source = models.CharField(_('Source'), max_length=60, choices=SOURCES, default=FRESH)

    @transition(field=status, source=FRESH,
                target=FORM_PENDING, permission=is_sales_user)
    def document_pending(self):
        print("changing the state from fresh to document pending")

    @transition(field=status, source=FRESH,
                target=APPROVED, permission=is_sales_user)
    def pending_form(self):
        print("changing the state from fresh to document pending")

    @transition(field=status, source=FRESH,
                target=APPROVED, permission=is_sales_user)
    def approve(self):
        print("changing the state from fresh to Approved")

    @transition(field=status, source=APPROVED,
                target=CONVERTED, permission=is_sales_user)
    def convert(self):
        LeadUser(name=self.name, phone_number=self.phone_number).save()
        print("changing the state from approved to converted")

