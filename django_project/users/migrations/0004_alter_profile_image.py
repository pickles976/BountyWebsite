# Generated by Django 3.2.14 on 2022-07-26 02:33

from django.db import migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=sorl.thumbnail.fields.ImageField(upload_to='profile_pics'),
        ),
    ]
