# Generated by Django 4.1.5 on 2023-04-24 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0002_user_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='nick_name',
            new_name='nick_name_user',
        ),
    ]
