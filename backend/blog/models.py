from django.db import models
from tinymce import models as tinymce_models
from django.contrib.flatpages.models import FlatPage
from django.contrib.auth.models import User, Group
from taggit.managers import TaggableManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django import forms

import datetime


class BlogPost(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200, null=False, blank=False)
    subtitle = models.CharField(max_length=1000)
    slug = models.SlugField(
        max_length=100, blank=True, null=True, help_text=_("Auto generated from title "
                                                           "field and date "
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


class BlogPostAdminForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['author', 'title', 'subtitle', 'slug', 'content', 'tags', 'published',
                  'featured']

    def clean(self):

        title = self.cleaned_data["title"]
        slug = self.cleaned_data['slug']

        if BlogPost.objects.filter(title=title).exists():
            date = datetime.datetime.today()
            self.cleaned_data['slug'] = '%s-%i-%i-%i' % (slug, date.year, date.month,
                                                         date.day)

        slug = self.cleaned_data['slug']
        if BlogPost.objects.filter(slug=slug).exists():
            raise forms.ValidationError({'slug': 'Slug already exists. Enter unique slug'})

        return self.cleaned_data
