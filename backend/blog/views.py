"""
These view functions and classes implement API endpoints
"""
from django.shortcuts import render
from blog.models import BlogPost


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
    posts = BlogPost.objects.filter(slug=slug)
    if not posts or (not posts[0].published and request.user != posts[0].author):
        return render(request, 'blog/blog_404.html')  # Respond with 404 page
    tags = posts[0].tags.names()
    context = {'post': posts[0], 'tags': tags}
    return render(request, 'blog/post.html', context)
