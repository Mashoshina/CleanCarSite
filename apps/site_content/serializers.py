from rest_framework import serializers

from .models import AboutUsBullet, AboutUsFeature, AboutUsSection


class AboutUsBulletSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUsBullet
        fields = ("id", "text", "sort_order")


class AboutUsFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUsFeature
        fields = ("id", "title", "description", "sort_order")


class AboutUsSectionSerializer(serializers.ModelSerializer):
    bullets = AboutUsBulletSerializer(many=True, read_only=True)
    features = AboutUsFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = AboutUsSection
        fields = ("title", "subtitle", "description", "bullets", "features")