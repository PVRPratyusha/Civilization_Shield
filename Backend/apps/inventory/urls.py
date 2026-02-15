from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'items', views.InventoryViewSet)
router.register(r'warehouses', views.WarehouseViewSet)

urlpatterns = [
    path('calculate/', views.CalculateSuppliesView.as_view()),
    path('resource-needs/', views.ResourceNeedsView.as_view()),
    path('', include(router.urls)),
]
