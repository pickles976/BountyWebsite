# Generated by Django 3.2.14 on 2022-07-23 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bounty', '0002_auto_20220722_2009'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Region',
        ),
        migrations.AddField(
            model_name='bounty',
            name='region',
            field=models.CharField(choices=[('ACRITHIA', 'Acrithia'), ('ALLODS', "Allod's Bight"), ('ASHFIELDS', 'Ash Fields'), ('BASIN', 'Basin Sionnach'), ('CALLAHAN', "Callahan's Passage"), ('CALLUMS', "Callum's Cape"), ('CLANSHEAD', 'Clanshead Valley'), ('ENDLESS', 'Endless Shore'), ('FARRANAC', 'Farranac Coast'), ('FISHERMANS', "Fisherman's Row"), ('GODCROFTS', 'Godcrofts'), ('GREATMARCH', 'Great March'), ('HOWL', 'Howl County'), ('KALOKAI', 'Kalokai'), ('LOCH', 'Loch Mór'), ('MARBAN', 'Marban Hollow'), ('MORGENS', "Morgen's Crossing"), ('NEVISH', 'Nevish Line'), ('ORIGIN', 'Origin'), ('REACHING', 'Reaching Trail'), ('REDRIVER', 'Red River'), ('SHACKLED', 'Shackled Chasm'), ('SPEAKING', 'Speaking Woods'), ('STONECRADLE', 'Stonecradle'), ('TEMPEST', 'Tempest Island'), ('TERMINUS', 'Terminus'), ('DEADLANDS', 'The Deadlands'), ('DROWNED', 'The Drowned Vale'), ('FINGERS', 'The Fingers'), ('HEARTLANDS', 'The Heartlands'), ('LINN', 'The Linn of Mercy'), ('MOORS', 'The Moors'), ('OARBREAKER', 'The Oarbreaker Isles'), ('UMBRAL', 'Umbral Wildwood'), ('VIPER', 'Viper Pit'), ('WEATHERED', 'Weathered Expanse'), ('WESTGATE', 'Westgate')], default='ASHFIELDS', max_length=32),
        ),
    ]