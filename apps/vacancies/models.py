
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify


class Vacancy(models.Model):
    """Вакансия сети автомоек CleanCar."""

    class Schedule(models.TextChoices):
        FIVE_TWO = "5/2", "5/2"
        TWO_TWO = "2/2", "2/2"

    class Experience(models.TextChoices):
        NO_EXPERIENCE = "no_experience", "Без опыта"
        THREE_PLUS_YEARS = "3_plus_years", "От 3 лет"

    name = models.CharField(
        max_length=150,
        verbose_name="Название вакансии",
    )
    schedule = models.CharField(
        max_length=10,
        choices=Schedule.choices,
        verbose_name="График работы",
    )
    salary = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="Зарплата",
    )
    experience = models.CharField(
        max_length=20,
        choices=Experience.choices,
        verbose_name="Опыт работы",
    )
    requirements = models.TextField(
        verbose_name="Требования",
    )
    has_night_shifts = models.BooleanField(
        default=False,
        verbose_name="Ночные смены",
    )
    slug = models.SlugField(
        max_length=180,
        unique=True,
        blank=True,
        verbose_name="Slug",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name, allow_unicode=True)
            slug = base_slug
            suffix = 2

            while (
                Vacancy.objects.filter(slug=slug)
                .exclude(pk=self.pk)
                .exists()
            ):
                slug = f"{base_slug}-{suffix}"
                suffix += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
        ordering = ["name"]
