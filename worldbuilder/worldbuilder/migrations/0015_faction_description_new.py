# Generated by Django 4.2.9 on 2024-01-23 19:29

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('worldbuilder', '0014_faction_description_rendered_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='faction',
            name='description_new',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Description'),
        ),
    ]
