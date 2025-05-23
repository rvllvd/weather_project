from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/weather/", views.weather_view, name="weather_api"),
    path("api/autocomplete/", views.autocomplete_view, name="autocomplete_api"),
    path("api/history/", views.history_view, name="history_api"),
]
