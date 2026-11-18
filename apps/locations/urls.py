from django.urls import path

from .views import LocationDetailView, LocationListView

urlpatterns = [
    path("", LocationListView.as_view(), name="location-list"),
    path("<slug:slug>/", LocationDetailView.as_view(), name="location-detail"),
]