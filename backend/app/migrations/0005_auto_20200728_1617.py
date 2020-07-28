# Generated by Django 3.0.8 on 2020-07-28 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_mapsquare_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mapsquare',
            name='photo',
        ),
        migrations.AddField(
            model_name='mapsquare',
            name='photo',
            field=models.ManyToManyField(blank=True, to='app.Photo'),
        ),
    ]
