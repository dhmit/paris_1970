# Generated by Django 3.2.14 on 2023-09-14 19:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_photo_model_add_folder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='contains_sticker',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='librarian_caption',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='photographer_caption',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='shelfmark',
        ),
        migrations.AddField(
            model_name='photo',
            name='full_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='location',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='alt',
            field=models.CharField(blank=True, max_length=252, null=True),
        ),
        migrations.AlterField(
            model_name='photoanalysisresult',
            name='photo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='analyses', to='app.photo'),
        ),
    ]