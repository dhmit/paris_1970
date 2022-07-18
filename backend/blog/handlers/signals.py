from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def add_user_to_group(sender, instance: User, created, **kwargs):
    try:
        if created:
            group = Group.objects.get(name="Blog Writers")
            instance.groups.add(group)
            instance.is_staff = True
            instance.save()
    except Group.DoesNotExist:
        pass



