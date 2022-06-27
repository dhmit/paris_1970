"""
These view functions and classes implement API endpoints
"""
from django.shortcuts import render
from .models import BlogPost


# app views
def index(request):
    """
    Home page
    """
    posts = BlogPost.objects.all()
    context = {'posts': posts}
    return render(request, 'cms_index.html', context)
