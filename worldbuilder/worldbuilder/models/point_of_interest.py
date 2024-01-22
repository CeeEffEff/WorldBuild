from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

class PointOfInterest(models.Model):
    class Meta:
        verbose_name = _("Point of Interest")
        verbose_name_plural = _("Points of Interest")

    name = models.CharField(max_length=50, null=False)
    description = models.TextField(null=True, blank=True)
    thumbnail = models.ImageField(
        upload_to="thumbnails/",
        default='thumbnails/default.jpeg',
        null=True
    )

    poi_map = models.ForeignKey(
        "Map",
        models.SET_NULL,
        blank=True,
        null=True,
        related_name="poi_map"
    )

    parent_maps = models.ManyToManyField(
        "Map",
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
