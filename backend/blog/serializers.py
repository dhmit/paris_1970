import json
from rest_framework import serializers
from config.settings import BLOG_ROOT_URL

from .models import (
    BlogPost,
    BlogPostAdminForm
)


class BlogPostSerializer(serializers.ModelSerializer):
    """
       Serializes a blog post
    """
    absolute_url = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    @staticmethod
    def get_absolute_url(instance):
        return f"/{BLOG_ROOT_URL}/{instance.slug}"

    @staticmethod
    def get_author(instance):
        return f"{instance.author}"

    class Meta:
        model = BlogPost
        fields = [
            'id', 'author', 'title', 'subtitle', 'slug', 'content', 'tags', 'published',
            'featured', 'date', 'absolute_url'
        ]