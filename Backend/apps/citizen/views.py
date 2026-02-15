"""Citizen Portal API Views"""
from rest_framework import viewsets, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

from services import NWSService, FEMAService
from .models import Shelter


class ShelterSerializer(serializers.ModelSerializer):
    available = serializers.ReadOnlyField()
    
    class Meta:
        model = Shelter
        fields = '__all__'


class SafetyStatusView(APIView):
    """Current safety status"""
    
    def get(self, request):
        state = request.query_params.get('state', settings.DEFAULT_STATE)
        
        alerts = NWSService.get_alerts(state=state, severity=['Extreme', 'Severe'])
        count = alerts.get('count', 0) if alerts.get('success') else 0
        
        if count > 0:
            extreme = sum(1 for a in alerts.get('alerts', []) if a.get('severity') == 'Extreme')
            if extreme:
                level, color, msg = 'critical', '#FF4D4D', 'CRITICAL: Extreme weather alert!'
            else:
                level, color, msg = 'warning', '#FFAA00', 'WARNING: Severe weather in area'
        else:
            level, color, msg = 'safe', '#00D68F', 'No severe alerts active'
        
        return Response({
            'success': True,
            'data': {
                'level': level,
                'color': color,
                'message': msg,
                'alertCount': count
            }
        })


class CitizenAlertsView(APIView):
    """Alerts for citizens"""
    
    def get(self, request):
        state = request.query_params.get('state', settings.DEFAULT_STATE)
        alerts = NWSService.get_alerts(state=state)
        
        if alerts.get('success'):
            # Simplify for citizens
            simplified = [{
                'type': a.get('event'),
                'severity': a.get('severity'),
                'headline': a.get('headline'),
                'instruction': a.get('instruction', 'Monitor local news'),
            } for a in alerts.get('alerts', [])[:10]]
            
            return Response({
                'success': True,
                'count': len(simplified),
                'alerts': simplified
            })
        return Response(alerts)


class EmergencyContactsView(APIView):
    """Emergency contacts"""
    
    def get(self, request):
        return Response({
            'success': True,
            'contacts': [
                {'name': 'Emergency', 'number': '911', 'type': 'emergency'},
                {'name': 'Non-Emergency', 'number': '211', 'type': 'info'},
                {'name': 'FEMA', 'number': '1-800-621-3362', 'type': 'assistance'},
                {'name': 'Red Cross', 'number': '1-800-733-2767', 'type': 'assistance'},
                {'name': 'Poison Control', 'number': '1-800-222-1222', 'type': 'medical'},
            ]
        })


class ShelterViewSet(viewsets.ModelViewSet):
    """Shelter management"""
    queryset = Shelter.objects.all()
    serializer_class = ShelterSerializer
    
    def get_queryset(self):
        qs = Shelter.objects.all()
        state = self.request.query_params.get('state')
        open_only = self.request.query_params.get('open')
        
        if state:
            qs = qs.filter(state=state)
        if open_only == 'true':
            qs = qs.filter(is_open=True)
        return qs


class FEMASheltersView(APIView):
    """FEMA shelters from API"""
    
    def get(self, request):
        state = request.query_params.get('state', settings.DEFAULT_STATE)
        return Response(FEMAService.get_shelters(state))


class AllSheltersView(APIView):
    """Combined local + FEMA shelters"""
    
    def get(self, request):
        state = request.query_params.get('state', settings.DEFAULT_STATE)
        
        # Local
        local = ShelterSerializer(
            Shelter.objects.filter(state=state, is_open=True),
            many=True
        ).data
        
        # FEMA
        fema_data = FEMAService.get_shelters(state)
        fema = fema_data.get('shelters', []) if fema_data.get('success') else []
        
        return Response({
            'success': True,
            'local': local,
            'fema': fema,
            'total': len(local) + len(fema)
        })
