"""
These view functions and classes implement API endpoints
"""
from django.shortcuts import render
from .models import Post, Category


# app views
def index(request):
    """
    Home page
    """
    posts = Post.objects.all()
    tags = Category.objects.all()
    context = {'posts': posts,'tags': tags}
    return render(request, 'cms_index.html', context)
