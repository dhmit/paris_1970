from django.db import models
from tinymce import models as tinymce_models
from django.contrib.flatpages.models import FlatPage
from django.contrib.auth.models import User, Group
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


class BlogPost(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200, null=False, blank=False)
    subtitle = models.CharField(max_length=1000)
    slug = models.SlugField(
        max_length=100, blank=True, null=True, help_text=_("Auto generated from title field "
                                                           "if not defined.")
    )
    content = tinymce_models.HTMLField()
    tags = TaggableManager(blank=True)
    published = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    # TODO: Maybe add related blogposts field?

    def get_absolute_url(self):
        # TODO
        return ""

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(BlogPost, self).save(*args, **kwargs)


# content_type = ContentType.objects.get_for_model(BlogPost)
#
# permission = Permission.objects.filter(content_type=content_type)
#
# BlogGroup = Group.objects.get_or_create(name="Blog Writer")
# # permission_list=["add_blogpost","change_blogpost","delete_blogpost","view_blogpost"]
# BlogGroup.permissions.set(permission)
