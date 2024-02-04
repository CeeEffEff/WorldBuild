from django.db import migrations


def save_text_rendered(apps, schema_editor):
    for model_name in ('Faction', 'Npc', 'PointOfInterest'):
        ModelWithRender = apps.get_model('worldbuilder', model_name)
        for examplemodel in ModelWithRender.objects.all():
            examplemodel.save()


class Migration(migrations.Migration):

    dependencies = [
        ('worldbuilder', '0018_remove_faction_description_new'),
    ]

    operations = [
        migrations.RunPython(save_text_rendered),
    ]
