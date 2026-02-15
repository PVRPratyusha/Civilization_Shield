"""Citizen models - Shelters"""
from django.db import models


class Shelter(models.Model):
    """Local shelter data"""
    
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=10)
    
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    capacity = models.IntegerField()
    occupancy = models.IntegerField(default=0)
    
    is_open = models.BooleanField(default=False)
    is_pet_friendly = models.BooleanField(default=False)
    is_ada_compliant = models.BooleanField(default=True)
    
    phone = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)
    
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['state', 'city', 'name']
    
    def __str__(self):
        status = "Open" if self.is_open else "Closed"
        return f"{self.name} ({status})"
    
    @property
    def available(self):
        return max(0, self.capacity - self.occupancy)
