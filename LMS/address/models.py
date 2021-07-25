from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.contrib.gis.db import models as gis_model


class UserAddress(models.Model):
    MR, MISS, MRS, MS, DR = ('Mr', 'Miss', 'Mrs', 'Ms', 'Dr')
    TITLE_CHOICES = (
        (MR, _("Mr")),
        (MISS, _("Miss")),
        (MRS, _("Mrs")),
        (MS, _("Ms")),
        (DR, _("Dr")),
    )

    POSTCODES_REGEX = {
        'IN': r'^[0-9]{6}$'
    }

    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='addresses', null=True, blank=True,
        verbose_name=_("User"))

    phone_number = PhoneNumberField(
        _("Phone number"), blank=True,
        help_text=_("In case we need to call you about your order"))

    #: Whether this address is the default for shipping
    is_default_for_shipping = models.BooleanField(
        _("Default shipping address?"), default=False)

    geopoint = gis_model.PointField(null=True, blank=True, srid=4326, help_text=_(
        "Represented as (longitude, latitude)"))

    title = models.CharField(
        pgettext_lazy("Treatment Pronouns for the customer", "Title"),
        max_length=64, choices=TITLE_CHOICES, blank=True)

    first_name = models.CharField(_("First name"), max_length=255, blank=True)
    last_name = models.CharField(_("Last name"), max_length=255, blank=True)

    # We use quite a few lines of an address as they are often quite long and
    # it's easier to just hide the unnecessary ones than add extra ones.
    line1 = models.CharField(_("First line of address"), max_length=255)
    line2 = models.CharField(
        _("Second line of address"), max_length=255, blank=True)
    line3 = models.CharField(
        _("Third line of address"), max_length=255, blank=True)
    line4 = models.CharField(_("City"), max_length=255, blank=True)

    state = models.CharField(_("State/County"), max_length=255, blank=True)

    postcode = models.CharField(_("Post/Zip-code"), max_length=64, blank=True)

    # country = models.ForeignKey('address.Country', on_delete=models.PROTECT, verbose_name=_("Country"))

    city = models.ForeignKey('address.City', on_delete=models.PROTECT, verbose_name=_("City"))

    # objects = UserAddressManager()

    def save(self, *args, **kwargs):
        super(UserAddress, self).save(*args, **kwargs)


class City(models.Model):
    name = models.CharField(_("Name"), max_length=255, unique=True)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(_("Name"), max_length=255, unique=True)