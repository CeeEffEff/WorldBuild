# Generated by Django 4.2.8 on 2023-12-26 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worldbuilder', '0002_map_description_map_map_name_map_scale'),
    ]

    operations = [
        migrations.AddField(
            model_name='map',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='worldbuilder.map'),
        ),
    ]
