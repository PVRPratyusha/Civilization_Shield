"""
FEMA OpenFEMA API
https://www.fema.gov/api/open - No API key required
"""
import requests
from datetime import datetime, timedelta
from cachetools import TTLCache


class FEMAService:
    BASE_URL = "https://www.fema.gov/api/open"
    
    _cache = TTLCache(maxsize=50, ttl=3600)  # 1 hour cache
    
    @classmethod
    def get_disasters(cls, state=None, days=30, limit=50):
        """Get disaster declarations"""
        cache_key = f"disasters_{state}_{days}"
        if cache_key in cls._cache:
            return cls._cache[cache_key]
        
        cutoff = (datetime.utcnow() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        params = {
            '$filter': f"declarationDate ge '{cutoff}'",
            '$orderby': 'declarationDate desc',
            '$top': limit
        }
        if state:
            params['$filter'] += f" and state eq '{state}'"
        
        try:
            resp = requests.get(f"{cls.BASE_URL}/v2/DisasterDeclarationsSummaries", params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            
            disasters = [{
                'number': d.get('disasterNumber'),
                'title': d.get('declarationTitle'),
                'type': d.get('incidentType'),
                'state': d.get('state'),
                'date': d.get('declarationDate'),
                'area': d.get('designatedArea'),
            } for d in data.get('DisasterDeclarationsSummaries', [])]
            
            result = {'success': True, 'source': 'FEMA', 'count': len(disasters), 'disasters': disasters}
            cls._cache[cache_key] = result
            return result
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @classmethod
    def get_shelters(cls, state=None):
        """Get open emergency shelters"""
        cache_key = f"shelters_{state}"
        if cache_key in cls._cache:
            return cls._cache[cache_key]
        
        params = {'$top': 500}
        if state:
            params['$filter'] = f"state eq '{state}'"
        
        try:
            resp = requests.get(f"{cls.BASE_URL}/v1/OpenShelters", params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            
            shelters = [{
                'id': s.get('shelter_id'),
                'name': s.get('shelter_name'),
                'address': s.get('address'),
                'city': s.get('city'),
                'state': s.get('state'),
                'zip': s.get('zip'),
                'lat': s.get('latitude'),
                'lon': s.get('longitude'),
                'capacity': s.get('evacuation_capacity'),
                'population': s.get('total_population'),
                'pets': s.get('accepting_pets'),
                'ada': s.get('ada_compliant'),
            } for s in data.get('OpenShelters', [])]
            
            result = {
                'success': True,
                'source': 'FEMA',
                'count': len(shelters),
                'shelters': shelters,
                'note': 'Availability varies by active disasters'
            }
            cls._cache[cache_key] = result
            return result
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @classmethod
    def get_statistics(cls, state=None, years=10):
        """Get disaster statistics for analytics"""
        cache_key = f"stats_{state}_{years}"
        if cache_key in cls._cache:
            return cls._cache[cache_key]
        
        cutoff_year = datetime.utcnow().year - years
        
        params = {
            '$filter': f"fyDeclared ge {cutoff_year}",
            '$top': 1000,
            '$select': 'disasterNumber,incidentType,state,fyDeclared'
        }
        if state:
            params['$filter'] += f" and state eq '{state}'"
        
        try:
            resp = requests.get(f"{cls.BASE_URL}/v2/DisasterDeclarationsSummaries", params=params, timeout=20)
            resp.raise_for_status()
            data = resp.json()
            
            disasters = data.get('DisasterDeclarationsSummaries', [])
            
            by_year = {}
            by_type = {}
            for d in disasters:
                year = d.get('fyDeclared')
                dtype = d.get('incidentType')
                by_year[year] = by_year.get(year, 0) + 1
                by_type[dtype] = by_type.get(dtype, 0) + 1
            
            result = {
                'success': True,
                'source': 'FEMA',
                'total': len(disasters),
                'by_year': dict(sorted(by_year.items())),
                'by_type': dict(sorted(by_type.items(), key=lambda x: x[1], reverse=True))
            }
            cls._cache[cache_key] = result
            return result
        except Exception as e:
            return {'success': False, 'error': str(e)}
