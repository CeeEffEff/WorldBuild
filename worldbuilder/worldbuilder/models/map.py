from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

class Map(models.Model):
    class Scale(models.TextChoices):
        ENCOUNTER = "EN", _("Encounter")
        SETTLEMENT = "SE", _("Settlement")
        PROVINCE = "PR", _("Province")
        KINGDOM = "KI", _("Kingdom")
        CONTINENT = "CO", _("Continent")
    SCALE_MAP = {
        Scale.ENCOUNTER: 0,
        Scale.SETTLEMENT: 1,
        Scale.PROVINCE: 2,
        Scale.KINGDOM: 3,
        Scale.CONTINENT: 4,
    }
    SCALE_DESCRIPTIONS = {
        Scale.ENCOUNTER: Scale.ENCOUNTER.label,
        Scale.SETTLEMENT: Scale.SETTLEMENT.label,
        Scale.PROVINCE: Scale.PROVINCE.label,
        Scale.KINGDOM: Scale.KINGDOM.label,
        Scale.CONTINENT: Scale.CONTINENT.label,
    }
    SCALE_MAP_REVERSE = { value: key for key, value in SCALE_MAP }

    map_name = models.CharField(max_length=50, null=False)
    image = models.ImageField(upload_to="maps/")
    description = models.TextField(null=True)
    scale = models.CharField(
        max_length=2,
        choices=Scale.choices,
        default=Scale.ENCOUNTER,
    )
    parent = models.ForeignKey(
        "self",
        models.SET_NULL,
        blank=True,
        null=True,
    )
    @property
    def scale_num(self) -> int:
        return self.SCALE_MAP[self.scale]
    @property
    def scale_friendly(self) -> str:
        return self.SCALE_DESCRIPTIONS[self.scale]

    @property
    def parent_scale(self) -> str:
        return self.SCALE_MAP_REVERSE.get(self.scale_num - 1)

    def __str__(self):
        return self.map_name

    def clean(self):
        if self.parent_scale and self.parent and not (self.parent.scale == self.parent_scale):
            raise ValidationError(
                { 'parent' : _(f'Parent Map must be one scale lever higher, i.e {self.parent_scale}')}
            )

class PointOfInterest(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.TextField(null=True)

    poi_map = models.ForeignKey(
        Map,
        models.SET_NULL,
        blank=True,
        null=True,
        related_name="poi_map"
    )

    parent_maps = models.ManyToManyField(
        Map,
        through="PoiOnMap",
        related_name="points_of_interest"
    )

    def __str__(self):
        return self.name

    # def clean(self):
    #     if self.parent_scale and self.parent and not (self.parent.scale == self.parent_scale):
    #         raise ValidationError(
    #             { 'parent' : _(f'Parent Map must be one scale lever higher, i.e {self.parent_scale}')}
    #         )

class PoiOnMap(models.Model):
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    point_of_interest = models.ForeignKey(PointOfInterest, on_delete=models.CASCADE)
    x = models.IntegerField()
    y = models.IntegerField()
    
    def __str__(self):
        return f'{self.point_of_interest} on {self.map}'
    
    def clean(self):
        if self.x < 0 or self.x >self.map.image.width:
            raise ValidationError(
                { 'x' : _(f'Point of interest is out-of-bounds')}
            )
        if self.y < 0 or self.y >self.map.image.height:
            raise ValidationError(
                { 'y' : _(f'Point of interest is out-of-bounds')}
            )
    
    class Meta:
        unique_together = ('map', 'point_of_interest')

