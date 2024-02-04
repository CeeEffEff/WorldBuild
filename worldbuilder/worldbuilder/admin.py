from django.contrib import admin
import worldbuilder.models as models
# Register your models here.

class QuestTaskInline(admin.TabularInline):
    model = models.QuestTask
    extra = 1

class QuestAdmin(admin.ModelAdmin):
    inlines = [
        QuestTaskInline,
    ]

admin.site.register([
        models.Map,
        models.PoiOnMap,
        models.PointOfInterest,
        models.Faction,
        models.Npc,
        models.QuestTask,
])
admin.site.register(
    models.Quest, QuestAdmin
)
