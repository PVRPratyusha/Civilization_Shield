"""
Load demo data for prototype
Run: python manage.py load_demo_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone

from apps.dashboard.models import Alert, Incident
from apps.logistics.models import Vehicle
from apps.inventory.models import InventoryItem, Warehouse
from apps.citizen.models import Shelter


class Command(BaseCommand):
    help = 'Load demo data'
    
    def handle(self, *args, **options):
        self.stdout.write('\n🚀 Loading demo data...\n')
        
        # Admin user
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@demo.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('✓ Admin user created (admin/admin123)'))
        
        # Vehicles
        vehicles = [
            {'vehicle_id': 'AMB-001', 'vehicle_type': 'ambulance', 'status': 'available', 'driver_name': 'John Smith'},
            {'vehicle_id': 'AMB-002', 'vehicle_type': 'ambulance', 'status': 'en_route', 'driver_name': 'Sarah Johnson', 'destination': 'Memorial Hospital'},
            {'vehicle_id': 'TRK-001', 'vehicle_type': 'supply_truck', 'status': 'available', 'driver_name': 'Mike Davis'},
            {'vehicle_id': 'TRK-002', 'vehicle_type': 'supply_truck', 'status': 'en_route', 'driver_name': 'Maria Garcia', 'destination': 'Central Warehouse'},
            {'vehicle_id': 'FIR-001', 'vehicle_type': 'fire_truck', 'status': 'available', 'driver_name': 'Robert Wilson'},
        ]
        for v in vehicles:
            Vehicle.objects.update_or_create(vehicle_id=v['vehicle_id'], defaults=v)
        self.stdout.write(self.style.SUCCESS(f'✓ {len(vehicles)} vehicles'))
        
        # Inventory
        items = [
            {'name': 'Water', 'category': 'hydration', 'unit': 'gallons', 'current_stock': 50000, 'minimum_stock': 30000, 'per_person_per_day': 1.0, 'guideline_source': 'FEMA', 'guideline_note': '1 gal/person/day'},
            {'name': 'Rice/Grains', 'category': 'food', 'unit': 'lbs', 'current_stock': 15000, 'minimum_stock': 10000, 'per_person_per_day': 0.3, 'guideline_source': 'USDA'},
            {'name': 'Canned Protein', 'category': 'food', 'unit': 'cans', 'current_stock': 8000, 'minimum_stock': 5000, 'per_person_per_day': 0.5},
            {'name': 'Canned Vegetables', 'category': 'food', 'unit': 'cans', 'current_stock': 6000, 'minimum_stock': 4000, 'per_person_per_day': 0.6},
            {'name': 'First Aid Kits', 'category': 'medical', 'unit': 'kits', 'current_stock': 500, 'minimum_stock': 300, 'per_household': 1.0, 'guideline_source': 'Red Cross'},
            {'name': 'Blankets', 'category': 'shelter', 'unit': 'units', 'current_stock': 2000, 'minimum_stock': 1000, 'per_person_per_day': 0.5},
        ]
        for i in items:
            InventoryItem.objects.update_or_create(name=i['name'], defaults=i)
        self.stdout.write(self.style.SUCCESS(f'✓ {len(items)} inventory items'))
        
        # Warehouses
        warehouses = [
            {'name': 'Central Distribution', 'address': '1000 Main St, Austin, TX', 'latitude': 30.2672, 'longitude': -97.7431, 'capacity': 100000, 'utilization': 65},
            {'name': 'North Warehouse', 'address': '500 North Loop, Austin, TX', 'latitude': 30.3500, 'longitude': -97.7200, 'capacity': 50000, 'utilization': 45},
        ]
        for w in warehouses:
            Warehouse.objects.update_or_create(name=w['name'], defaults=w)
        self.stdout.write(self.style.SUCCESS(f'✓ {len(warehouses)} warehouses'))
        
        # Shelters
        shelters = [
            {'name': 'Austin Convention Center', 'address': '500 E Cesar Chavez St', 'city': 'Austin', 'state': 'TX', 'zip_code': '78701', 'latitude': 30.2630, 'longitude': -97.7396, 'capacity': 5000, 'is_pet_friendly': True, 'is_ada_compliant': True},
            {'name': 'Palmer Events Center', 'address': '900 Barton Springs Rd', 'city': 'Austin', 'state': 'TX', 'zip_code': '78704', 'latitude': 30.2600, 'longitude': -97.7520, 'capacity': 3000, 'is_ada_compliant': True},
            {'name': 'Travis County Expo', 'address': '7311 Decker Ln', 'city': 'Austin', 'state': 'TX', 'zip_code': '78724', 'latitude': 30.3094, 'longitude': -97.6450, 'capacity': 8000, 'is_pet_friendly': True, 'is_ada_compliant': True},
        ]
        for s in shelters:
            Shelter.objects.update_or_create(name=s['name'], defaults=s)
        self.stdout.write(self.style.SUCCESS(f'✓ {len(shelters)} shelters'))
        
        # Sample incident
        Incident.objects.update_or_create(
            description='Multi-vehicle accident on I-35',
            defaults={
                'incident_type': 'traffic',
                'severity': 'moderate',
                'status': 'confirmed',
                'location': 'I-35 at 51st Street',
                'latitude': 30.3100,
                'longitude': -97.7200
            }
        )
        self.stdout.write(self.style.SUCCESS('✓ Sample incident'))
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('✅ Demo data loaded!'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write('')
        self.stdout.write('🔑 Admin: admin / admin123')
        self.stdout.write('🌐 Admin Panel: http://localhost:8000/admin/')
        self.stdout.write('📡 API: http://localhost:8000/api/v1/')
        self.stdout.write('')
