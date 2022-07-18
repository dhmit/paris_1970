from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from blog.models import BlogPost


class Command(BaseCommand):
    help = 'Help with group creation'

    def handle(self, *args, **options):
        blog_group, created = Group.objects.get_or_create(name="Blog Writers")

        content_type = ContentType.objects.get_for_model(BlogPost)

        permissions = Permission.objects.filter(content_type=content_type)

        blog_group.permissions.set(permissions)


