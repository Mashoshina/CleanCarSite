# apps/announcements/models.py
from django.db import models


class Announcement(models.Model):
    """Объявление."""

    class ActiveStatus(models.IntegerChoices):
        ACTIVE = 0, "Активно"
        INACTIVE = 1, "Не активно"

    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок",
    )
    content = models.TextField(
        verbose_name="Суть",
    )
    status = models.PositiveSmallIntegerField(
        choices=ActiveStatus.choices,
        default=ActiveStatus.ACTIVE,
        verbose_name="Статус",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["title"]