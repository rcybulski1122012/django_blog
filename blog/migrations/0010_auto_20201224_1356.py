# Generated by Django 3.1.4 on 2020-12-24 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_post_likes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='published',
            new_name='is_published',
        ),
    ]
