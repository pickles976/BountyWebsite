# Generated by Django 3.2.14 on 2022-07-23 15:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bounty', '0005_bounty_job_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Acceptance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bounty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bounty.bounty')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]