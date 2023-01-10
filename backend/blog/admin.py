from django.contrib import admin
from django.conf import settings
from django.utils.safestring import mark_safe

from tinymce.widgets import TinyMCE

from blog.models import BlogPost
from blog.forms import BlogPostAdminForm

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['id', 'custom_slug', 'title', 'subtitle', 'author']
    form = BlogPostAdminForm
    # TODO: make slug be a link that takes the admin user to the blog page

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'content':
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
                # mce_attrs={'external_link_list_url': reverse('tinymce-linklist')},
            ))
        return super().formfield_for_dbfield(db_field, **kwargs)

    def custom_slug(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            "/" + settings.BLOG_ROOT_URL + "/" + obj.slug, obj.slug))

    custom_slug.short_description = "Slug (preview on site)"


admin.site.register(BlogPost, BlogPostAdmin)
