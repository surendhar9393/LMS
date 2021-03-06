from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from rest_framework_jwt.settings import api_settings


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserManager(BaseUserManager):
    """
    Custom manager for create user
    """

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Create and Save an User with email and password
            :param str email: user email
            :param str password: user password
            :param bool is_staff: whether user staff or not
            :param bool is_superuser: whether user admin or not
            :return users.models.User user: user
            :raise ValueError: email is not set
        """
        now = timezone.now()

        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)

        is_active = extra_fields.pop("is_active", False)

        user = self.model(email=email, is_staff=is_staff, is_active=is_active,
                          is_superuser=is_superuser, last_login=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save an User with email and password
        :param str email: user email
        :param str password: user password
        :return users.models.User user: regular user
        """
        is_staff = extra_fields.pop("is_staff", False)
        return self._create_user(email, password, is_staff, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save an User with the given email and password.
        :param str email: user email
        :param str password: user password
        :return users.models.User user: admin user
        """
        return self._create_user(email, password, True, True, is_active=True,
                                 **extra_fields)

    def do_login(self, request, user_name, password):
        """
            Returns the JWT token in case of success, returns the error
            response in case of login failed.
        """
        user = authenticate(email=user_name, password=password)

        return user

    def generate_auth_token(self, user):
        # Generating the JWT Token
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(
        _('Name of User'), max_length=255)

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        db_index=True
    )

    is_staff = models.BooleanField(
        _('staff status'), default=False, help_text=_(
            'Designates whether the user can log into this admin site.'))

    is_active = models.BooleanField(_('active'), default=False, help_text=_(
        'Designates whether this user should be treated as '
        'active. Unselect this instead of deleting accounts.'))

    phone_number = PhoneNumberField(
        _("Mobile Number"), blank=True, unique=True,
        help_text=_("Customer's primary mobile number e.g. +91{10 digit mobile number}"))

    objects = UserManager()

    USERNAME_FIELD = 'email'


class LeadUser(models.Model):
    """
    Lead User are created once leads are converted
    """
    name = models.CharField(
        _('Name of User'), max_length=255)

    is_active = models.BooleanField(_('active'), default=False)

    phone_number = PhoneNumberField(
        _("Mobile Number"), blank=True, unique=True,
        help_text=_("Customer's primary mobile number e.g. +91{10 digit mobile number}"))
