from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

class PoiOnMap(models.Model):
    map = models.ForeignKey("Map", on_delete=models.CASCADE)
    point_of_interest = models.ForeignKey("PointOfInterest", on_delete=models.CASCADE)
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