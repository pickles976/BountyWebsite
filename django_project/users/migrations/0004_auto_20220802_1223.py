# Generated by Django 3.2.14 on 2022-08-02 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20220802_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='dateAuthorized',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='discordToken',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]