# Generated by Django 4.1.5 on 2023-05-30 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0011_alter_post_user_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='champion',
            field=models.CharField(max_length=200),
        ),
    ]
