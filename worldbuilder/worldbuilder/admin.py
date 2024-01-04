from django.contrib import admin
from worldbuilder.models import map
# Register your models here.
admin.site.register([
        map.Map,
        map.PoiOnMap,
        map.PointOfInterest
])
