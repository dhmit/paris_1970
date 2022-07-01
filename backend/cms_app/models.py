"""
Models for the paris_1970 app.

"""
from django.db import models


class Category(models.Model):
    tag = models.CharField(max_length=20, help_text="Enter blog category")

    def __str__(self):
        return self.tag


class Post(models.Model):
    title = models.CharField(max_length=100)
    category = models.ManyToManyField(Category,help_text="Select blog category")
    profession = models.CharField(max_length=50, default="STUDENT POST")
    author = models.CharField(max_length=50, default='Author name')
    featured = models.BooleanField(default=None)
    image = models.ImageField(upload_to='img')
    body = models.TextField(default='body')
    published = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField()

    def __str__(self):
        return self.title
