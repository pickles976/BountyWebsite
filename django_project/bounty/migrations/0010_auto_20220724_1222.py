# Generated by Django 3.2.14 on 2022-07-24 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bounty', '0009_auto_20220724_1040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bounty',
            name='num_submissions',
        ),
        migrations.RemoveField(
            model_name='bounty',
            name='price',
        ),
    ]