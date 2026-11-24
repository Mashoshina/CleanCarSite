from django.db import models


class AboutUsSection(models.Model):
    title = models.CharField(max_length=150, default="О нас", verbose_name="Заголовок")
    subtitle = models.CharField(
        max_length=255,
        default="Мы в ответе за свой сервис",
        verbose_name="Подзаголовок",
    )
    description = models.TextField(
        default=(
            "На рынке уже 20 лет, и всё это время задаем стандарты "
            "автомобильного ухода. CleanCar — это сеть автомоек нового "
            "поколения, где вам всегда рады."
        ),
        verbose_name="Описание",
    )
    is_published = models.BooleanField(default=True, verbose_name="Опубликован")

    class Meta:
        verbose_name = "Раздел «О нас»"
        verbose_name_plural = "Раздел «О нас»"

    def __str__(self):
        return self.title


class AboutUsBullet(models.Model):
    section = models.ForeignKey(
        AboutUsSection,
        on_delete=models.CASCADE,
        related_name="bullets",
        verbose_name="Раздел",
    )
    text = models.CharField(max_length=255, verbose_name="Текст")
    sort_order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Пункт списка"
        verbose_name_plural = "Пункты списка"

    def __str__(self):
        return self.text


class AboutUsFeature(models.Model):
    section = models.ForeignKey(
        AboutUsSection,
        on_delete=models.CASCADE,
        related_name="features",
        verbose_name="Раздел",
    )
    title = models.CharField(max_length=150, verbose_name="Заголовок карточки")
    description = models.TextField(verbose_name="Описание карточки")
    sort_order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Карточка преимущества"
        verbose_name_plural = "Карточки преимуществ"

    def __str__(self):
        return self.title