import json
from rest_framework import serializers

from .models import (
    BlogPost,
    BlogPostAdminForm
)


class BlogPostSerializer(serializers.ModelSerializer):
    """
       Serializes a blog post
    """

    class Meta:
        model = BlogPost
        fields = [
            'id', 'author', 'title', 'subtitle', 'slug', 'content', 'tags', 'published',
            'featured', 'date'
        ]
