"""
These view functions and classes implement API endpoints
"""
from django.shortcuts import render
from djangocms_blog.models import Post
# from .models import Category


# app views
def index(request):
    """
    Home page
    """
    posts = Post.objects.all()
    print("index getting called", posts)
    # tags = Category.objects.all()
    context = {'posts': posts}
    return render(request, 'cms_index.html', context)
