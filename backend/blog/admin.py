from django.contrib import admin
from .models import BlogPost, BlogPostAdminForm
from tinymce.widgets import TinyMCE


class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm
    list_display = ['id', 'slug', 'title', 'subtitle', 'author']
    prepopulated_fields = {'slug': ('title',)}

    # TODO: make slug be a link that takes the admin user to the blog page

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'content':
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
                # mce_attrs={'external_link_list_url': reverse('tinymce-linklist')},
            ))
        return super().formfield_for_dbfield(db_field, **kwargs)


admin.site.register(BlogPost, BlogPostAdmin)
