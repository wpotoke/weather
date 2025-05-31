from django.urls import path
from weather import views
from .api_views import Autocomplete, CityStatsView



urlpatterns = [
    path('', views.index, name="index"),
    path('api/autocomplete/', Autocomplete.as_view(), name='autocomplete'),
    path('api/stats/', CityStatsView.as_view(), name="stats"),
]
