from django.contrib import admin
from .models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['vehicle_id', 'vehicle_type', 'status', 'driver_name', 'destination', 'last_updated']
    list_filter = ['vehicle_type', 'status']
    list_editable = ['status']
    search_fields = ['vehicle_id', 'driver_name']
