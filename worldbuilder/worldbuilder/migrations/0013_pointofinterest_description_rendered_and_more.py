# Generated by Django 4.2.9 on 2024-01-23 14:05

from django.db import migrations
import markdownfield.models


class Migration(migrations.Migration):

    dependencies = [
        ('worldbuilder', '0012_alter_faction_icon_alter_npc_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pointofinterest',
            name='description_rendered',
            field=markdownfield.models.RenderedMarkdownField(null=True),
        ),
        migrations.AlterField(
            model_name='pointofinterest',
            name='description',
            field=markdownfield.models.MarkdownField(blank=True, null=True, rendered_field='description_rendered'),
        ),
    ]
