# Generated by Django 3.0.4 on 2020-07-20 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [
        ("ai_lab", "0011_auto_20200720_1435"),
        ("ai_lab", "0012_auto_20200720_1536"),
    ]

    dependencies = [
        ("ai_lab", "0010_auto_20200720_1431"),
        ("images", "0001_initial"),
        ("wagtailimages", "0001_squashed_0021"),
    ]

    operations = [
        migrations.AddField(
            model_name="ailabcasestudy",
            name="summary",
            field=models.CharField(default="", max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ailabexternalresource",
            name="summary",
            field=models.CharField(default="", max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ailabcasestudy",
            name="featured_image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.NHSXImage",
            ),
        ),
        migrations.AddField(
            model_name="ailabexternalresource",
            name="featured_image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.NHSXImage",
            ),
        ),
    ]
