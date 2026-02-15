"""Logistics API Views"""
from rest_framework import viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from .models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


class VehicleViewSet(viewsets.ModelViewSet):
    """Vehicle management"""
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    lookup_field = 'vehicle_id'
    
    @action(detail=True, methods=['put'])
    def position(self, request, vehicle_id=None):
        """Update vehicle position"""
        vehicle = self.get_object()
        vehicle.latitude = request.data.get('lat', vehicle.latitude)
        vehicle.longitude = request.data.get('lon', vehicle.longitude)
        vehicle.save()
        return Response(VehicleSerializer(vehicle).data)
    
    @action(detail=True, methods=['post'], url_path='dispatch')
    def dispatch_vehicle(self, request, vehicle_id=None):
        """Dispatch vehicle to destination"""
        vehicle = self.get_object()
        vehicle.destination = request.data.get('destination', '')
        vehicle.status = 'en_route'
        vehicle.dispatched_at = timezone.now()
        vehicle.save()
        return Response(VehicleSerializer(vehicle).data)
    
    def get_queryset(self):
        qs = Vehicle.objects.all()
        status = self.request.query_params.get('status')
        vtype = self.request.query_params.get('type')
        if status:
            qs = qs.filter(status=status)
        if vtype:
            qs = qs.filter(vehicle_type=vtype)
        return qs