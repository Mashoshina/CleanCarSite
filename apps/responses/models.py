from django.core.validators import RegexValidator
from django.db import models

from apps.vacancies.models import Vacancy


class Response(models.Model):
    """Отклик на вакансию."""

    vacancy = models.ForeignKey(
        Vacancy,
        on_delete=models.CASCADE,
        related_name="responses",
        verbose_name="Вакансия",
    )
    name = models.CharField(
        max_length=150,
        verbose_name="Имя",
    )
    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"^\+?[0-9\s\-\(\)]+$",
                message="Телефон должен содержать только цифры, пробелы, +, -, ()",
            )
        ],
        verbose_name="Телефон",
    )
    email = models.EmailField(
        verbose_name="Почта",
        validators=[
            RegexValidator(
                regex=r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@(?:[A-Za-z0-9-]+\.)?(?:ru|com)$",
                message="Email должен содержать домен .ru или .com",
            )
        ],
    )
    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name="Комментарий",
    )

    def __str__(self):
        return f"{self.name} — {self.vacancy}"

    class Meta:
        verbose_name = "Отклик"
        verbose_name_plural = "Отклики"
        ordering = ["-id"]