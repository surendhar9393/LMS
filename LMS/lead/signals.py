from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Lead
from LMS.user.models import User
import random


@receiver(post_save, sender=Lead)
def vendor_document_event(sender, instance, created, **kwargs):
    if created:
        users = User.objects.filter(groups__name__in=['Sales Executive (Calling team)', 'Sales Executive (Field Agent)',
                                                      'Sales Manager'], is_active=True, is_staff=True)
        if not users:
            users = User.objects.filter(is_active=True, is_staff=True)
        if users:
            users_count = users.count()
            user = users[random.randint(0, users_count - 1)]
            instance.action_owner_id = user.id
            instance.save()
