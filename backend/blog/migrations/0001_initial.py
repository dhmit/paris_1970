# Generated by Django 3.2.14 on 2022-07-08 01:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', tinymce.models.HTMLField()),
                ('slug', models.SlugField(max_length=100)),
                ('title', models.CharField(max_length=200)),
                ('published', models.BooleanField(default=False)),
                ('featured', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('subtitle', models.CharField(max_length=1000)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
