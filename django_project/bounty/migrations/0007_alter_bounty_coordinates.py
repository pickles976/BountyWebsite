# Generated by Django 3.2.14 on 2022-07-23 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bounty', '0006_acceptance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bounty',
            name='coordinates',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
    ]