"""Inventory models - Supplies and Warehouses"""
from django.db import models


class InventoryItem(models.Model):
    """Supply inventory"""
    
    CATEGORY_CHOICES = [
        ('hydration', 'Hydration'),
        ('food', 'Food'),
        ('medical', 'Medical'),
        ('shelter', 'Shelter'),
        ('equipment', 'Equipment'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    unit = models.CharField(max_length=20)
    
    current_stock = models.IntegerField(default=0)
    minimum_stock = models.IntegerField(default=0)
    
    # FEMA guidelines
    per_person_per_day = models.FloatField(null=True, blank=True)
    per_household = models.FloatField(null=True, blank=True)
    guideline_source = models.CharField(max_length=100, blank=True)
    guideline_note = models.TextField(blank=True)
    
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.current_stock} {self.unit})"
    
    @property
    def status(self):
        if self.current_stock <= 0:
            return 'critical'
        elif self.current_stock < self.minimum_stock:
            return 'low'
        return 'adequate'


class Warehouse(models.Model):
    """Supply warehouses"""
    
    STATUS_CHOICES = [
        ('operational', 'Operational'),
        ('limited', 'Limited'),
        ('offline', 'Offline'),
    ]
    
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    capacity = models.IntegerField()
    utilization = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='operational')
    
    def __str__(self):
        return self.name
