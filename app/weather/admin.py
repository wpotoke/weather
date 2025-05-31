from django.contrib import admin
from weather.models import CitySearch


# Register your models here.
@admin.register(CitySearch)
class CitySearchAdmin(admin.ModelAdmin):
    fields = ["city"]
