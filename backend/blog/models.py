import datetime
from django import forms
from django.db import models
from django.contrib.flatpages.models import FlatPage
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from tinymce import models as tinymce_models
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager
from django.utils.translation import gettext_lazy as _
from config.settings import BLOG_ROOT_URL


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
        return f"/{BLOG_ROOT_URL}/{self.slug}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(BlogPost, self).save(*args, **kwargs)


class BlogPostAdminForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['author', 'title', 'subtitle', 'slug', 'content', 'tags', 'published',
                  'featured']

    def slug_generator(self):
        title = self.cleaned_data["title"]
        date = datetime.datetime.today()
        self.cleaned_data['slug'] = '%s-%i-%i-%i' % (slugify(title), date.year, date.month,
                                                     date.day)
        slug = self.cleaned_data['slug']
        return slug

    def clean(self):
        slug = self.cleaned_data["slug"]

        if self.instance._state.adding is True:
            if slug is None:
                slug = self.slug_generator()
                if BlogPost.objects.filter(slug=slug).exists():
                    raise forms.ValidationError(
                        {'slug': 'Autogenerated slug already exists. Enter unique '
                                 'slug'})

            if BlogPost.objects.filter(slug=slug).exists():
                raise forms.ValidationError(
                    {"slug": "Slug already exists. Enter unique slug or leave empty"})
        else:

            if slug is None:
                slug = self.slug_generator()

            if BlogPost.objects.filter(slug=slug).exists() and slug != self.instance.slug:
                raise forms.ValidationError(
                    {"slug": "Slug already exists. Enter unique slug"})
