"""
These view functions and classes implement API endpoints
"""
from datetime import datetime
from django.utils import dateparse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from blog.models import (
    BlogPost
)

from .serializers import (
    BlogPostSerializer
)


def blog_home_page(request):
    posts = BlogPost.objects.all()
    # Set of all tags belonging to published posts
    tags = list(set([tag for post in posts for tag in post.tags.names() if post.published]))
    serialized_posts = BlogPostSerializer(posts, many=True)
    data = serialized_posts.data

    for post in data:
        post['tags'] = list(post['tags'].names())
        author_obj = User.objects.get(username=post['author'])
        post['author'] = author_obj.first_name + " " + author_obj.last_name
        date = dateparse.parse_datetime(post['date'])
        post['date'] = datetime.strftime(date, "%B %d, %Y")

    context = {
        'page_metadata': {
            'title': _('Blog Home Page')
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
    all_posts = BlogPost.objects.all()

    if posts and (
        posts[0].published
        or request.user == posts[0].author
        or request.user.has_perm('blog.view_blogpost')
        or request.user.is_superuser
    ):
        tags = list(posts[0].tags.names())
        post = posts[0]

        serialized_post = BlogPostSerializer(post)
        serialized_all_posts = BlogPostSerializer(all_posts, many=True)
        data = serialized_post.data
        date = dateparse.parse_datetime(data['date'])
        data['date'] = datetime.strftime(date, "%B %d, %Y")
        all_posts_data = serialized_all_posts.data

        for post in all_posts_data:
            author_obj = User.objects.get(username=post['author'])
            post['tags'] = list(post['tags'].names())
            post['author'] = author_obj.first_name + " " + author_obj.last_name

        data['tags'] = list(data['tags'].names())
        context = {
            'page_metadata': {
                'title': _('Blog Post') + ': ' + data['slug']
            },
            'component_name': 'BlogPost',
            'component_props': {
                'all_posts': all_posts_data,
                'post': data,
                'tags': tags
            }
        }
        return render_view(request, context)

    return render(request, 'blog/blog_404.html')  # Respond with 404 page


def render_view(request, context):
    context.setdefault('component_props', {})
    return render(request, 'index.html', context)
