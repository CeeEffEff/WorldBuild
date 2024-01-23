from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

class Npc(models.Model):

    class Meta:
        verbose_name = _("NPC")
        verbose_name_plural = _("NPCs")

    def __str__(self):
        return self.name

    name = models.CharField(max_length=50, null=False, blank=False)
    image = models.ImageField(upload_to="npcs/", null=True, blank=True)
    alignment = models.TextField(_("Alignment"), null=True, blank=True)
    classes = models.TextField(_("Classes"),  null=True, blank=True)
    description = models.TextField(_("Description"), null=True, blank=True)
    goals = models.TextField(_("Individual Goals"),  null=True, blank=True)
    # quests = models.ManyToManyField("Quest", verbose_name=_("Faction Quests"))
    points_of_interest = models.ManyToManyField("PointOfInterest", verbose_name=_("Points of Interest"))
