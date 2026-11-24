from django.contrib import admin

from .models import AboutUsBullet, AboutUsFeature, AboutUsSection


class AboutUsBulletInline(admin.TabularInline):
    model = AboutUsBullet
    extra = 1


class AboutUsFeatureInline(admin.TabularInline):
    model = AboutUsFeature
    extra = 1


@admin.register(AboutUsSection)
class AboutUsSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published")
    list_editable = ("is_published",)
    inlines = (AboutUsBulletInline, AboutUsFeatureInline)

    def has_add_permission(self, request):
        # Для этой страницы достаточно одной записи-раздела.
        return not AboutUsSection.objects.exists()