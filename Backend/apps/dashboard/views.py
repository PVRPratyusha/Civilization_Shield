"""Dashboard API Views"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import serializers
from django.conf import settings

from services import NWSService, FEMAService
from .models import Alert, Incident


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'


class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = '__all__'


class StatsView(APIView):
    """Dashboard statistics"""
    
    def get(self, request):
        state = request.query_params.get('state', settings.DEFAULT_STATE)
        
        # Real NWS alerts
        nws_data = NWSService.get_alerts(state=state)
        alert_count = nws_data.get('count', 0) if nws_data.get('success') else 0
        
        # Real FEMA disasters
        fema_data = FEMAService.get_disasters(state=state, days=30)
        disaster_count = fema_data.get('count', 0) if fema_data.get('success') else 0
        
        # Local data
        local_alerts = Alert.objects.filter(status='active').count()
        active_incidents = Incident.objects.exclude(status='resolved').count()
        
        return Response({
            'success': True,
            'data': {
                'weatherAlerts': alert_count,
                'recentDisasters': disaster_count,
                'localAlerts': local_alerts,
                'activeIncidents': active_incidents,
            },
            'sources': ['NWS', 'FEMA', 'Local DB']
        })


class WeatherAlertsView(APIView):
    """Get NWS weather alerts"""
    
    def get(self, request):
        state = request.query_params.get('state', settings.DEFAULT_STATE)
        severity = request.query_params.get('severity')
        
        severity_list = severity.split(',') if severity else None
        return Response(NWSService.get_alerts(state=state, severity=severity_list))


class WeatherForecastView(APIView):
    """Get NWS weather forecast"""
    
    def get(self, request):
        lat = float(request.query_params.get('lat', settings.DEFAULT_LAT))
        lon = float(request.query_params.get('lon', settings.DEFAULT_LON))
        return Response(NWSService.get_forecast(lat, lon))


class DisastersView(APIView):
    """Get FEMA disasters"""
    
    def get(self, request):
        state = request.query_params.get('state')
        days = int(request.query_params.get('days', 30))
        return Response(FEMAService.get_disasters(state=state, days=days))


class AlertViewSet(viewsets.ModelViewSet):
    """Local alerts CRUD"""
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer


class IncidentViewSet(viewsets.ModelViewSet):
    """Incidents CRUD"""
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    
    def get_queryset(self):
        qs = Incident.objects.all()
        status = self.request.query_params.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs
