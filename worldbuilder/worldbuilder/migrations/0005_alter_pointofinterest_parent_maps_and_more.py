# Generated by Django 4.2.8 on 2024-01-06 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worldbuilder', '0004_pointofinterest_poionmap_pointofinterest_parent_maps_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pointofinterest',
            name='parent_maps',
            field=models.ManyToManyField(related_name='points_of_interest', through='worldbuilder.PoiOnMap', to='worldbuilder.map'),
        ),
        migrations.AlterUniqueTogether(
            name='poionmap',
            unique_together={('map', 'point_of_interest')},
        ),
    ]
