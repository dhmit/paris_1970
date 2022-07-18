"""
These view functions and classes implement API endpoints
"""
from django.shortcuts import render
from blog.models import BlogPost
from taggit.models import Tag


def index(request):
    """
    Blog home page
    """
    posts = BlogPost.objects.all()
    tags = Tag.objects.all()
    print(posts)
    context = {'posts': posts, 'tags': tags}
    return render(request, 'blog/home.html', context)


def blog_post(request, slug):
    """
    Single blog post view
    """
    post = BlogPost.objects.get(slug=slug)
    tags = Tag.objects.all()
    context = {'post': post, 'tags': tags}
    return render(request, 'blog/post.html', context)
