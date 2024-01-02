from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
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
