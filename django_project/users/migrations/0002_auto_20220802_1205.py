# Generated by Django 3.2.14 on 2022-08-02 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bounty', '0006_guild'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileimage',
            name='dateAuthorized',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='profileimage',
            name='discordToken',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='profileimage',
            name='guilds',
            field=models.ManyToManyField(to='bounty.Guild'),
        ),
    ]
