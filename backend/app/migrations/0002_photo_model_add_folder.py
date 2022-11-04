# Generated by Django 3.2.14 on 2022-10-28 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='folder',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='photo',
            name='number',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='photo',
            unique_together={('number', 'folder', 'map_square')},
        ),
    ]
