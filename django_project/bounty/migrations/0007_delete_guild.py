# Generated by Django 3.2.14 on 2022-08-02 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_profile_guilds'),
        ('bounty', '0006_guild'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Guild',
        ),
    ]
