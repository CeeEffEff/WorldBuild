# Generated by Django 4.2.9 on 2024-01-23 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worldbuilder', '0010_alter_faction_description_alter_faction_founder_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faction',
            name='icon',
            field=models.ImageField(null=True, upload_to='factions/'),
        ),
    ]
