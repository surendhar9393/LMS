from LMS.user.models import User


def is_sales_user(instance, user):
    return User.objects.filter(user=user, groups__name__in=['Sales Executive (Calling team)', 'Sales Executive (Field Agent)',
                                          'Sales Manager'], is_active=True, is_staff=True).exists()
