# Generated by Django 4.2.9 on 2024-01-23 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worldbuilder', '0011_alter_faction_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faction',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='factions/'),
        ),
        migrations.AlterField(
            model_name='npc',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='npcs/'),
        ),
        migrations.AlterField(
            model_name='pointofinterest',
            name='thumbnail',
            field=models.ImageField(blank=True, default='thumbnails/default.jpeg', null=True, upload_to='thumbnails/'),
        ),
        migrations.AlterField(
            model_name='quest',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='quests/'),
        ),
    ]