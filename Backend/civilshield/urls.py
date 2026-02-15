"""
URL Configuration for Civilization Shield
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'service': 'Civilization Shield API',
        'version': '1.0.0'
    })


def api_root(request):
    return JsonResponse({
        'message': 'Civilization Shield API',
        'endpoints': {
            'dashboard': '/api/v1/dashboard/',
            'logistics': '/api/v1/logistics/',
            'inventory': '/api/v1/inventory/',
            'citizen': '/api/v1/citizen/',
            'analytics': '/api/v1/analytics/',
        },
        'admin': '/admin/',
        'docs': 'Use Django REST Framework browsable API'
    })


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Health check
    path('api/v1/health/', health_check),
    
    # API Root
    path('api/v1/', api_root),
    
    # App endpoints
    path('api/v1/dashboard/', include('apps.dashboard.urls')),
    path('api/v1/logistics/', include('apps.logistics.urls')),
    path('api/v1/inventory/', include('apps.inventory.urls')),
    path('api/v1/citizen/', include('apps.citizen.urls')),
    path('api/v1/analytics/', include('apps.analytics.urls')),
]

# Admin customization
admin.site.site_header = "Civilization Shield Admin"
admin.site.site_title = "Crisis Management"
admin.site.index_title = "Dashboard"
