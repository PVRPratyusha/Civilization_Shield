"""
US Census Bureau API
https://api.census.gov - No API key required (500 req/day)
"""
import requests
from cachetools import TTLCache
from django.conf import settings


class CensusService:
    BASE_URL = "https://api.census.gov/data"
    
    _cache = TTLCache(maxsize=100, ttl=86400)  # 24 hour cache
    
    STATE_FIPS = {
        'AL': '01', 'AK': '02', 'AZ': '04', 'AR': '05', 'CA': '06',
        'CO': '08', 'CT': '09', 'DE': '10', 'DC': '11', 'FL': '12',
        'GA': '13', 'HI': '15', 'ID': '16', 'IL': '17', 'IN': '18',
        'IA': '19', 'KS': '20', 'KY': '21', 'LA': '22', 'ME': '23',
        'MD': '24', 'MA': '25', 'MI': '26', 'MN': '27', 'MS': '28',
        'MO': '29', 'MT': '30', 'NE': '31', 'NV': '32', 'NH': '33',
        'NJ': '34', 'NM': '35', 'NY': '36', 'NC': '37', 'ND': '38',
        'OH': '39', 'OK': '40', 'OR': '41', 'PA': '42', 'RI': '44',
        'SC': '45', 'SD': '46', 'TN': '47', 'TX': '48', 'UT': '49',
        'VT': '50', 'VA': '51', 'WA': '53', 'WV': '54', 'WI': '55',
        'WY': '56', 'PR': '72'
    }
    
    @classmethod
    def get_population(cls, state_code):
        """Get state population"""
        cache_key = f"pop_{state_code}"
        if cache_key in cls._cache:
            return cls._cache[cache_key]
        
        fips = cls.STATE_FIPS.get(state_code.upper())
        if not fips:
            return {'success': False, 'error': f'Invalid state: {state_code}'}
        
        params = {'get': 'NAME,B01003_001E', 'for': f'state:{fips}'}
        
        api_key = getattr(settings, 'CENSUS_API_KEY', None)
        if api_key:
            params['key'] = api_key
        
        try:
            resp = requests.get(f"{cls.BASE_URL}/2021/acs/acs5", params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            
            if len(data) > 1:
                result = {
                    'success': True,
                    'source': 'Census Bureau',
                    'state': data[1][0],
                    'population': int(data[1][1])
                }
                cls._cache[cache_key] = result
                return result
            return {'success': False, 'error': 'No data'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @classmethod
    def calculate_resources(cls, state_code, days=7):
        """Calculate emergency resource needs based on FEMA guidelines"""
        pop_data = cls.get_population(state_code)
        if not pop_data.get('success'):
            return pop_data
        
        population = pop_data['population']
        affected = int(population * 0.05)  # 5% emergency planning baseline
        households = affected // 4
        
        return {
            'success': True,
            'source': 'Census + FEMA Guidelines',
            'state': state_code,
            'total_population': population,
            'affected_estimate': affected,
            'days': days,
            'resources': {
                'water_gallons': affected * days * 1,
                'food_calories': affected * days * 2000,
                'first_aid_kits': households,
                'shelter_beds': int(affected * 0.1),
            },
            'guidelines': {
                'water': '1 gallon/person/day (FEMA)',
                'food': '2000 calories/person/day (USDA)',
                'first_aid': '1 kit/household (Red Cross)',
                'shelter': '~10% may need shelter'
            }
        }
