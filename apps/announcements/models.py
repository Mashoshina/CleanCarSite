# apps/announcements/models.py
from django.db import models


class Announcement(models.Model):
    """Объявление."""

    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок",
    )
    content = models.TextField(
        verbose_name="Суть",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активно",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["title"]