from rest_framework import serializers

from .models import (
    BlogPost
)


class BlogPostSerializer(serializers.ModelSerializer):
    """
       Serializes a blog post
    """
    absolute_url = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    @staticmethod
    def get_absolute_url(instance):
        return f"/blog/{instance.slug}"

    @staticmethod
    def get_author(instance):
        return f"{instance.author}"

    class Meta:
        model = BlogPost
        fields = [
            'id', 'author', 'title', 'subtitle', 'slug', 'content', 'tags', 'published',
            'featured', 'date', 'absolute_url'
        ]
