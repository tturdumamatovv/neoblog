# Generated by Django 5.0 on 2023-12-28 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_post_favorites'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='total_comments',
            field=models.IntegerField(default=0),
        ),
    ]
