from django.contrib import admin
import worldbuilder.models as models

# Register your models here.


class QuestTaskInline(admin.TabularInline):
    model = models.QuestTask
    extra = 1


@admin.register(models.Quest)
class QuestAdmin(admin.ModelAdmin):
    inlines = [
        QuestTaskInline,
    ]


@admin.register(models.Faction)
class FactionAdmin(admin.ModelAdmin):
    filter_horizontal = ["notable_members", "points_of_interest"]


@admin.register(models.Npc)
class NpcAdmin(admin.ModelAdmin):
    filter_horizontal = ["points_of_interest"]


class PoiOnMapInline(admin.TabularInline):
    model = models.PoiOnMap
    extra = 1  # how many rows to show


@admin.register(models.PointOfInterest)
class PointOfInterestAdmin(admin.ModelAdmin):
    inlines = [PoiOnMapInline]


admin.site.register(
    [
        models.Map,
        models.PoiOnMap,
        models.QuestTask,
    ]
)
