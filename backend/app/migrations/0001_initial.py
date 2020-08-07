# Generated by Django 3.0.8 on 2020-08-07 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MapSquare',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=252)),
                ('number', models.IntegerField(null=True)),
                ('boundaries', models.CharField(max_length=252)),
            ],
        ),
        migrations.CreateModel(
            name='Photographer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=252)),
                ('number', models.IntegerField(null=True)),
                ('type', models.CharField(max_length=252)),
                ('sentiment', models.CharField(max_length=252)),
                ('map_square', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.MapSquare')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(null=True)),
                ('shelfmark', models.CharField(max_length=252)),
                ('contains_sticker', models.BooleanField(null=True)),
                ('front_src', models.CharField(max_length=252)),
                ('back_src', models.CharField(max_length=252)),
                ('alt', models.CharField(max_length=252)),
                ('librarian_caption', models.CharField(max_length=252)),
                ('photographer_caption', models.CharField(max_length=252)),
                ('map_square', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.MapSquare')),
                ('photographer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.Photographer')),
            ],
        ),
    ]
