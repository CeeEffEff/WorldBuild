from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

class Quest(models.Model):

    class Meta:
        verbose_name = _("Quest")
        verbose_name_plural = _("Quests")

    def __str__(self):
        return self.name

    name = models.CharField(max_length=50, null=False, blank=False)
    image = models.ImageField(upload_to="quests/", null=True, blank=True)
    description = models.TextField(_("Description"), null=True, blank=True)
    faction = models.ManyToManyField("Faction", verbose_name=_("Quest Faction"))
    quest_giver = models.ManyToManyField("Npc", verbose_name=_("Quest Giver"))
    rewards = models.TextField(_("Rewards"), null=True, blank=True)

    @property
    def progress(self) -> str:
        num_tasks = len(self.tasks)
        if num_tasks == 0:
            return 'N/A'
        completed = sum((task.complete for task in self.tasks))
        return f'{((completed / num_tasks) * 100):.2f}%'

class QuestTask(models.Model):

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")

    def __str__(self):
        return self.name

    name = models.CharField(max_length=50, null=False, blank=False)
    criteria = models.TextField(_("Criteria"), null=True, blank=True)
    points_of_interest = models.ManyToManyField("PointOfInterest", verbose_name=_("Points of Interest"))
    complete = models.BooleanField(_("Complete"), default=False)
    quest = models.ForeignKey('Quest', related_name="tasks", null=False, on_delete=models.DO_NOTHING)
