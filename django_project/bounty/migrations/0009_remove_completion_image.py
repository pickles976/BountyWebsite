# Generated by Django 3.2.14 on 2022-08-14 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bounty', '0008_alter_bounty_jobtype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='completion',
            name='image',
        ),
    ]