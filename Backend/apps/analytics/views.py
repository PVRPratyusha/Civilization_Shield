"""
Analytics API Views
- Disaster Forecasting
- Risk Scoring
- Shelter Recommendations
- Anomaly Detection
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from datetime import datetime
import math

from services import NWSService, FEMAService, CensusService
from apps.citizen.models import Shelter


class DisasterForecastView(APIView):
    """Forecast disasters using FEMA historical data"""
    
    def get(self, request):
        state = request.query_params.get('state')
        months = int(request.query_params.get('months', 6))
        
        # Get historical data
        stats = FEMAService.get_statistics(state, years=10)
        if not stats.get('success'):
            return Response(stats)
        
        by_year = stats.get('by_year', {})
        if len(by_year) < 3:
            return Response({'error': 'Insufficient historical data'}, status=400)
        
        # Calculate average
        years = sorted(by_year.keys())
        counts = [by_year[y] for y in years]
        avg = sum(counts) / len(counts)
        
        # Simple trend
        n = len(counts)
        if n > 1:
            trend = (counts[-1] - counts[0]) / n
        else:
            trend = 0
        
        # Project forward with seasonal adjustment
        projections = []
        current_year = datetime.now().year
        current_month = datetime.now().month
        
        for i in range(months):
            month = (current_month + i - 1) % 12 + 1
            year = current_year + (current_month + i - 1) // 12
            
            # Seasonal factor (higher in spring/fall)
            seasonal = {1: 0.7, 2: 0.7, 3: 1.0, 4: 1.3, 5: 1.3, 6: 1.1,
                       7: 1.0, 8: 1.4, 9: 1.5, 10: 1.3, 11: 0.9, 12: 0.7}
            
            base = (avg / 12) + (trend * i / 12)
            predicted = base * seasonal.get(month, 1.0)
            
            projections.append({
                'month': f"{year}-{month:02d}",
                'predicted': round(max(0, predicted), 2),
                'seasonal_factor': seasonal.get(month, 1.0)
            })
        
        return Response({
            'success': True,
            'data': {
                'state': state,
                'historical': {
                    'years_analyzed': len(years),
                    'total': stats.get('total'),
                    'avg_per_year': round(avg, 1),
                    'trend': 'increasing' if trend > 0.5 else 'decreasing' if trend < -0.5 else 'stable'
                },
                'by_type': stats.get('by_type'),
                'projections': projections
            },
            'methodology': 'Linear trend + seasonal adjustment'
        })


class RiskScoreView(APIView):
    """Calculate area risk score"""
    
    def get(self, request):
        state = request.query_params.get('state', settings.DEFAULT_STATE)
        
        # Current alerts (40% weight)
        alerts = NWSService.get_alerts(state=state)
        if alerts.get('success'):
            count = alerts.get('count', 0)
            severe = sum(1 for a in alerts.get('alerts', []) if a.get('severity') in ['Extreme', 'Severe'])
            alert_score = min(100, severe * 25 + count * 10)
        else:
            alert_score = 0
        
        # Historical disasters (40% weight)
        history = FEMAService.get_statistics(state, years=5)
        if history.get('success'):
            total = history.get('total', 0)
            history_score = min(100, total * 3)
        else:
            history_score = 0
        
        # Population vulnerability (20% weight)
        census = CensusService.get_population(state)
        if census.get('success'):
            pop = census.get('population', 0)
            # Higher population = more at risk
            pop_score = min(100, pop / 500000)
        else:
            pop_score = 50
        
        # Weighted average
        overall = alert_score * 0.4 + history_score * 0.4 + pop_score * 0.2
        
        if overall >= 60:
            level, color = 'high', '#FF4D4D'
        elif overall >= 30:
            level, color = 'moderate', '#FFAA00'
        else:
            level, color = 'low', '#00D68F'
        
        return Response({
            'success': True,
            'data': {
                'state': state,
                'score': round(overall, 1),
                'level': level,
                'color': color,
                'factors': {
                    'current_alerts': round(alert_score, 1),
                    'historical': round(history_score, 1),
                    'population': round(pop_score, 1)
                },
                'recommendations': self._get_recommendations(level, alert_score)
            }
        })
    
    def _get_recommendations(self, level, alert_score):
        recs = []
        if level == 'high':
            recs.append('Review emergency plans immediately')
            recs.append('Ensure supplies are stocked')
        if alert_score > 50:
            recs.append('Monitor weather alerts continuously')
        if not recs:
            recs.append('Maintain standard preparedness')
        return recs


class ShelterRecommendView(APIView):
    """Recommend shelters based on location and needs"""
    
    def get(self, request):
        lat = float(request.query_params.get('lat', settings.DEFAULT_LAT))
        lon = float(request.query_params.get('lon', settings.DEFAULT_LON))
        state = request.query_params.get('state', settings.DEFAULT_STATE)
        needs_ada = request.query_params.get('needs_ada', 'false').lower() == 'true'
        has_pets = request.query_params.get('has_pets', 'false').lower() == 'true'
        
        # Query shelters
        shelters = Shelter.objects.filter(state=state, is_open=True)
        
        if needs_ada:
            shelters = shelters.filter(is_ada_compliant=True)
        if has_pets:
            shelters = shelters.filter(is_pet_friendly=True)
        
        # Score shelters
        recommendations = []
        for s in shelters:
            distance = self._haversine(lat, lon, s.latitude, s.longitude)
            
            # Score: closer = better, bonuses for features
            score = max(0, 100 - distance * 5)
            if s.is_ada_compliant:
                score += 5
            if s.is_pet_friendly:
                score += 5
            if s.available > 100:
                score += 10
            
            recommendations.append({
                'name': s.name,
                'address': f"{s.address}, {s.city}, {s.state}",
                'distance_miles': round(distance, 2),
                'capacity': s.capacity,
                'available': s.available,
                'pet_friendly': s.is_pet_friendly,
                'ada_compliant': s.is_ada_compliant,
                'score': round(score, 1)
            })
        
        # Sort by score
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        return Response({
            'success': True,
            'data': {
                'location': {'lat': lat, 'lon': lon},
                'filters': {'needs_ada': needs_ada, 'has_pets': has_pets},
                'count': len(recommendations),
                'recommendations': recommendations[:5]
            }
        })
    
    def _haversine(self, lat1, lon1, lat2, lon2):
        """Distance in miles"""
        R = 3959
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        return R * 2 * math.asin(math.sqrt(a))


class AnomalyDetectView(APIView):
    """Detect anomalies in resource consumption"""
    
    def post(self, request):
        resource = request.data.get('resource', 'unknown')
        current = float(request.data.get('current_rate', 0))
        avg = float(request.data.get('historical_avg', 1))
        std = float(request.data.get('historical_std', 1))
        
        # Z-score
        z = (current - avg) / std if std > 0 else 0
        
        if abs(z) > 3:
            level = 'severe'
        elif abs(z) > 2:
            level = 'moderate'
        elif abs(z) > 1.5:
            level = 'mild'
        else:
            level = 'normal'
        
        return Response({
            'success': True,
            'data': {
                'resource': resource,
                'current': current,
                'average': avg,
                'z_score': round(z, 2),
                'level': level,
                'is_anomaly': level != 'normal',
                'direction': 'above' if current > avg else 'below',
                'deviation_pct': round(abs(current - avg) / avg * 100, 1) if avg else 0
            }
        })


class AnalyticsOverviewView(APIView):
    """List available analytics"""
    
    def get(self, request):
        return Response({
            'success': True,
            'endpoints': {
                'forecast': '/api/v1/analytics/forecast/disasters/',
                'risk': '/api/v1/analytics/risk/area/',
                'shelter': '/api/v1/analytics/recommend/shelter/',
                'anomaly': '/api/v1/analytics/anomaly/consumption/'
            },
            'algorithms': [
                'Time-series forecasting (trend + seasonal)',
                'Multi-factor risk classification',
                'Distance-based shelter scoring',
                'Z-score anomaly detection'
            ]
        })
