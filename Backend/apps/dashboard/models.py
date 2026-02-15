"""Dashboard models - Alerts and Stats tracking"""
from django.db import models
from django.utils import timezone


class Alert(models.Model):
    """Local alerts (supplements NWS data)"""
    
    SEVERITY_CHOICES = [
        ('minor', 'Minor'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
        ('extreme', 'Extreme'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('acknowledged', 'Acknowledged'),
        ('resolved', 'Resolved'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    source = models.CharField(max_length=50, default='local')
    external_id = models.CharField(max_length=100, blank=True)
    
    areas_affected = models.CharField(max_length=500, blank=True)
    instructions = models.TextField(blank=True)
    
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    effective_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-effective_at']
    
    def __str__(self):
        return f"{self.title} ({self.severity})"


class Incident(models.Model):
    """Reported incidents"""
    
    TYPE_CHOICES = [
        ('traffic', 'Traffic'),
        ('weather', 'Weather'),
        ('infrastructure', 'Infrastructure'),
        ('medical', 'Medical'),
        ('fire', 'Fire'),
        ('flood', 'Flooding'),
        ('other', 'Other'),
    ]
    
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('reported', 'Reported'),
        ('confirmed', 'Confirmed'),
        ('responding', 'Responding'),
        ('resolved', 'Resolved'),
    ]
    
    incident_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='moderate')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reported')
    
    description = models.TextField()
    location = models.CharField(max_length=200, blank=True)
    
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    reported_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-reported_at']
    
    def __str__(self):
        return f"{self.get_incident_type_display()} - {self.severity}"
