"""
These view functions and classes implement API endpoints
"""
import json

from django.core import serializers
from django.shortcuts import render

from blog.models import (
    BlogPost
)

from .serializers import (
    BlogPostSerializer
)


def index(request):
    """
    Blog home page
    """
    posts = BlogPost.objects.all()
    # Set of all tags belonging to published posts
    tags = set([tag for post in posts for tag in post.tags.names() if post.published])
    context = {'posts': posts, 'tags': tags}
    return render(request, 'blog/home.html', context)


def blog_page(request):
    posts = BlogPost.objects.all()
    # Set of all tags belonging to published posts
    tags = list(set([tag for post in posts for tag in post.tags.names() if post.published]))
    serialized_posts = BlogPostSerializer(posts, many=True)
    data = serialized_posts.data

    for post in data:
        post['tags'] = list(post['tags'].names())

    context = {
        'page_metadata': {
            'title': 'Blog Home Page'
        },
        'component_name': 'Blog',
        'component_props': {
            'posts': data,
            'tags': tags
        }
    }

    return render_view(request, context)


def blog_post(request, slug):
    """
    Single blog post view
    """
    posts = BlogPost.objects.filter(slug=slug)
    if posts and (
        posts[0].published
        or request.user == posts[0].author
        or request.user.has_perm('blog.view_blogpost')
        or request.user.is_superuser
    ):
        tags = posts[0].tags.names()
        post = posts[0]

        serialized_post = BlogPostSerializer(post)
        data = serialized_post.data

        data['tags'] = list(data['tags'].names())

        context = {
            'page_metadata': {
                'title': 'Blog Post: ' + data['slug']
            },
            'component_name': 'BlogPostView',
            'component_props': {
                'post': data,
                'tags': tags
            }
        }
        return render_view(request, context)

    return render(request, 'blog/blog_404.html')  # Respond with 404 page


def render_view(request, context):
    context.setdefault('component_props', {})
    return render(request, 'index.html', context)
