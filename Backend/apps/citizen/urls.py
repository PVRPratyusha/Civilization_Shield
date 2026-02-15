from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'shelters', views.ShelterViewSet)

urlpatterns = [
    path('safety-status/', views.SafetyStatusView.as_view()),
    path('alerts/', views.CitizenAlertsView.as_view()),
    path('emergency-contacts/', views.EmergencyContactsView.as_view()),
    path('shelters/fema/', views.FEMASheltersView.as_view()),
    path('shelters/all/', views.AllSheltersView.as_view()),
    path('', include(router.urls)),
]
