"""
National Weather Service API
https://api.weather.gov - No API key required
"""
import requests
from cachetools import TTLCache


class NWSService:
    BASE_URL = "https://api.weather.gov"
    HEADERS = {"User-Agent": "(CivilizationShield)", "Accept": "application/geo+json"}
    
    _cache = TTLCache(maxsize=100, ttl=300)  # 5 min cache
    
    @classmethod
    def get_alerts(cls, state=None, severity=None):
        """Get active weather alerts"""
        cache_key = f"alerts_{state}_{severity}"
        if cache_key in cls._cache:
            return cls._cache[cache_key]
        
        params = {}
        if state:
            params['area'] = state
        if severity:
            params['severity'] = ','.join(severity) if isinstance(severity, list) else severity
        
        try:
            resp = requests.get(f"{cls.BASE_URL}/alerts/active", headers=cls.HEADERS, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            
            alerts = [{
                'id': f.get('properties', {}).get('id'),
                'event': f.get('properties', {}).get('event'),
                'headline': f.get('properties', {}).get('headline'),
                'description': f.get('properties', {}).get('description'),
                'severity': f.get('properties', {}).get('severity'),
                'urgency': f.get('properties', {}).get('urgency'),
                'areas': f.get('properties', {}).get('areaDesc'),
                'instruction': f.get('properties', {}).get('instruction'),
                'expires': f.get('properties', {}).get('expires'),
            } for f in data.get('features', [])]
            
            result = {'success': True, 'source': 'NWS', 'count': len(alerts), 'alerts': alerts}
            cls._cache[cache_key] = result
            return result
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @classmethod
    def get_forecast(cls, lat, lon):
        """Get weather forecast for location"""
        cache_key = f"forecast_{lat}_{lon}"
        if cache_key in cls._cache:
            return cls._cache[cache_key]
        
        try:
            # Get grid point
            point_resp = requests.get(f"{cls.BASE_URL}/points/{lat},{lon}", headers=cls.HEADERS, timeout=10)
            point_resp.raise_for_status()
            point_data = point_resp.json()
            
            forecast_url = point_data.get('properties', {}).get('forecast')
            location = point_data.get('properties', {}).get('relativeLocation', {}).get('properties', {})
            
            # Get forecast
            forecast_resp = requests.get(forecast_url, headers=cls.HEADERS, timeout=10)
            forecast_resp.raise_for_status()
            forecast_data = forecast_resp.json()
            
            periods = [{
                'name': p.get('name'),
                'temperature': p.get('temperature'),
                'unit': p.get('temperatureUnit'),
                'wind': p.get('windSpeed'),
                'forecast': p.get('shortForecast'),
                'detailed': p.get('detailedForecast'),
            } for p in forecast_data.get('properties', {}).get('periods', [])]
            
            result = {
                'success': True,
                'source': 'NWS',
                'location': {'city': location.get('city'), 'state': location.get('state')},
                'periods': periods
            }
            cls._cache[cache_key] = result
            return result
        except Exception as e:
            return {'success': False, 'error': str(e)}
