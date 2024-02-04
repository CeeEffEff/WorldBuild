from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from django import forms
from django.templatetags.static import static
import worldbuilder.models as models
# Register your models here.

class QuestTaskInline(admin.TabularInline):
    model = models.QuestTask
    extra = 1

class QuestAdmin(admin.ModelAdmin):
    inlines = [
        QuestTaskInline,
    ]



class FactionAdminForm(forms.ModelForm):
    class Meta:
        model = models.Faction
        fields = '__all__'
        widgets = {
            'description_new': CKEditorWidget(),
        }

class FactionAdmin(admin.ModelAdmin):
    form = FactionAdminForm

    class Media:
        js = (
            "https://cdn.ckeditor.com/4.17.1/standard/ckeditor.js",
            static("ckeditor/ckeditor/plugins/insertlink/plugin.js"),
        )

admin.site.register(models.Faction, FactionAdmin)

admin.site.register([
        models.Map,
        models.PoiOnMap,
        models.PointOfInterest,
        models.Npc,
        models.QuestTask,
])
admin.site.register(
    models.Quest, QuestAdmin
)
