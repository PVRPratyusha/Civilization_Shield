"""Logistics models - Vehicles and Routes"""
from django.db import models


class Vehicle(models.Model):
    """Emergency vehicles"""
    
    TYPE_CHOICES = [
        ('ambulance', 'Ambulance'),
        ('fire_truck', 'Fire Truck'),
        ('supply_truck', 'Supply Truck'),
        ('rescue', 'Rescue'),
        ('command', 'Command'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('en_route', 'En Route'),
        ('on_scene', 'On Scene'),
        ('returning', 'Returning'),
        ('maintenance', 'Maintenance'),
    ]
    
    vehicle_id = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    driver_name = models.CharField(max_length=100, blank=True)
    
    latitude = models.FloatField(default=30.2672)
    longitude = models.FloatField(default=-97.7431)
    
    destination = models.CharField(max_length=200, blank=True)
    dispatched_at = models.DateTimeField(null=True, blank=True)
    
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-last_updated']
    
    def __str__(self):
        return f"{self.vehicle_id} ({self.get_vehicle_type_display()})"
