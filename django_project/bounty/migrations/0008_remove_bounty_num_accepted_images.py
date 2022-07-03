# Generated by Django 4.0.5 on 2022-07-02 23:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bounty', '0007_alter_bounty_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bounty',
            name='num_accepted',
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='bounty_images')),
                ('bounty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bounty.bounty')),
            ],
        ),
    ]