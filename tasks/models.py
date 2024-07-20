from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Task(models.Model):   # create table tasks_task (
    title = models.CharField(_("title"), max_length=255)
    is_done = models.BooleanField(_("is done"), default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"), on_delete=models.CASCADE)

    class Meta:
        db_table = "tasks"
        verbose_name = _("task")
        verbose_name_plural = _("tasks")

    def __str__(self):
        return self.title


# CRUD
# C: create
# R: retrieve   (list, details)
# U: update
# D: delete
