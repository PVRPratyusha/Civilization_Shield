"""Inventory API Views"""
from rest_framework import viewsets, serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from services import CensusService
from .models import InventoryItem, Warehouse


class InventoryItemSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField()
    
    class Meta:
        model = InventoryItem
        fields = '__all__'


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'


class InventoryViewSet(viewsets.ModelViewSet):
    """Inventory CRUD"""
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    
    def get_queryset(self):
        qs = InventoryItem.objects.all()
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category=category)
        return qs


class WarehouseViewSet(viewsets.ModelViewSet):
    """Warehouse CRUD"""
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


class CalculateSuppliesView(APIView):
    """Calculate required supplies"""
    
    def post(self, request):
        people = request.data.get('people')
        state = request.data.get('state')
        days = request.data.get('days', 7)
        
        # Get population from Census if state provided
        if state and not people:
            census_data = CensusService.get_population(state)
            if census_data.get('success'):
                people = int(census_data['population'] * 0.05)
        
        if not people:
            return Response({'error': 'people or state required'}, status=400)
        
        households = people // 4
        requirements = {'population': people, 'days': days, 'items': {}}
        
        for item in InventoryItem.objects.all():
            if item.per_person_per_day:
                required = people * days * item.per_person_per_day
            elif item.per_household:
                required = households * item.per_household
            else:
                continue
            
            shortage = max(0, required - item.current_stock)
            requirements['items'][item.name] = {
                'required': round(required),
                'current': item.current_stock,
                'shortage': round(shortage),
                'unit': item.unit,
                'guideline': item.guideline_note
            }
        
        return Response({'success': True, 'data': requirements})


class ResourceNeedsView(APIView):
    """Get resource needs by state"""
    
    def get(self, request):
        state = request.query_params.get('state', 'TX')
        days = int(request.query_params.get('days', 7))
        return Response(CensusService.calculate_resources(state, days))
