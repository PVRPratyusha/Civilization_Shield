from django.contrib import admin
from .models import Shelter


@admin.register(Shelter)
class ShelterAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'state', 'capacity', 'occupancy', 'is_open', 'is_pet_friendly']
    list_filter = ['state', 'is_open', 'is_pet_friendly', 'is_ada_compliant']
    list_editable = ['is_open', 'occupancy']
    search_fields = ['name', 'city', 'address']
