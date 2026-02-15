from django.contrib import admin
from .models import Alert, Incident


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['title', 'severity', 'status', 'source', 'effective_at']
    list_filter = ['severity', 'status', 'source']
    list_editable = ['status']
    search_fields = ['title', 'description']


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ['id', 'incident_type', 'severity', 'status', 'location', 'reported_at']
    list_filter = ['incident_type', 'severity', 'status']
    list_editable = ['status']
    search_fields = ['description', 'location']
