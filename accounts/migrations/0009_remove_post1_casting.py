# Generated by Django 2.2.1 on 2019-12-19 00:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_post1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post1',
            name='casting',
        ),
    ]
