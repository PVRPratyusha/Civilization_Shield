from django.contrib import admin
from .models import InventoryItem, Warehouse


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'current_stock', 'minimum_stock', 'unit', 'status']
    list_filter = ['category']
    list_editable = ['current_stock', 'minimum_stock']
    search_fields = ['name']
    
    def status(self, obj):
        return obj.status


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'capacity', 'utilization', 'status']
    list_filter = ['status']
    list_editable = ['status', 'utilization']
