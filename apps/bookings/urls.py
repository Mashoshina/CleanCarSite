from django.urls import path

from .views import BookingDeleteView, BookingListCreateView

urlpatterns = [
    path("", BookingListCreateView.as_view(), name="booking-list-create"),
    path("<int:pk>/", BookingDeleteView.as_view(), name="booking-delete"),
]