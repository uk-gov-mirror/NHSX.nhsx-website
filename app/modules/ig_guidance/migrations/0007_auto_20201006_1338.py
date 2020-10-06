# Generated by Django 3.0.7 on 2020-10-06 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ig_guidance', '0006_auto_20200922_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='igguidancetag',
            name='name',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='igguidancetag',
            name='slug',
            field=models.SlugField(max_length=60, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='igguidancetopic',
            name='name',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='igguidancetopic',
            name='slug',
            field=models.SlugField(max_length=60, null=True, unique=True),
        ),
    ]
