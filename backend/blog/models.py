from django.db import models
from tinymce import models as tinymce_models
from django.contrib.flatpages.models import FlatPage
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class BlogPost(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    content = tinymce_models.HTMLField()
    slug = models.SlugField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=200, null=False, blank=False)
    published = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    subtitle = models.CharField(max_length=1000)

    # TODO: add tags (taggit). Maybe add related blogposts field?

    def get_absolute_url(self):
        # TODO
        return ""

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(BlogPost, self).save(*args, **kwargs)
