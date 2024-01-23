from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from markdownfield.models import MarkdownField, RenderedMarkdownField
from markdownfield.validators import VALIDATOR_STANDARD
from ckeditor.fields import RichTextField

class Faction(models.Model):

    class Meta:
        verbose_name = _("Faction")
        verbose_name_plural = _("Factions")

    def __str__(self):
        return self.name

    name = models.CharField(max_length=50, null=False, blank=False)
    icon = models.ImageField(upload_to="factions/", null=True, blank=True)
    motto = models.CharField(max_length=100, null=True, blank=True)
    description_new = models.TextField(_("Description"), null=True, blank=True)
    description = MarkdownField(_("General Description"), rendered_field='description_rendered', validator=VALIDATOR_STANDARD, null=True, blank=True)
    description_rendered = RenderedMarkdownField(null=True, blank=True)
    goals = models.TextField(_("Goals"), null=True, blank=True)
    founder = models.ForeignKey("Npc", verbose_name=_("Founder"), on_delete=models.DO_NOTHING, related_name="founded_factions", null=True)
    leader = models.ForeignKey("Npc", verbose_name=_("Leader"), on_delete=models.DO_NOTHING, related_name="leader_of_factions", null=True)
    notable_members = models.ManyToManyField("Npc", verbose_name=_("Notable Members"), related_name="factions")
    typical_alignments = models.TextField(_("Typical Member Alignments"), null=True, blank=True)
    typical_classes = models.TextField(_("Typical Member Classes"), null=True, blank=True)
    typical_activities = models.TextField(_("Typical Member Activities"), null=True, blank=True)
    # quests = models.ManyToManyField("Quest", verbose_name=_("Faction Quests"))
    points_of_interest = models.ManyToManyField("PointOfInterest", verbose_name=_("Points of Interest"))
