from django.contrib import admin
# from django import forms
from django.contrib.flatpages.admin import FlatPageAdmin
from .models import BlogPost
from django.urls import reverse
from tinymce.widgets import TinyMCE


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['id', 'slug', 'title', 'subtitle', 'author']
    # TODO: make slug be a link that takes the admin user to the blog page

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'content':
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
                # mce_attrs={'external_link_list_url': reverse('tinymce-linklist')},
            ))
        return super().formfield_for_dbfield(db_field, **kwargs)


admin.site.register(BlogPost, BlogPostAdmin)
