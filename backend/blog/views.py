"""
These view functions and classes implement API endpoints
"""
from django.shortcuts import render
from blog.models import BlogPost
from django.http import Http404


def index(request):
    """
    Blog home page
    """
    posts = BlogPost.objects.all()
    # Set of all tags belonging to published posts
    tags = set([tag for post in posts for tag in post.tags.names() if post.published])
    context = {'posts': posts, 'tags': tags}
    return render(request, 'blog/home.html', context)


def blog_post(request, slug):
    """
    Single blog post view
    """
    post = BlogPost.objects.get(slug=slug)
    tags = post.tags.names()
    context = {'post': post, 'tags': tags}
    if not post.published and request.user != post.author:
        raise Http404
    return render(request, 'blog/post.html', context)
