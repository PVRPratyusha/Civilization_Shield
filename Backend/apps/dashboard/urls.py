from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'alerts', views.AlertViewSet)
router.register(r'incidents', views.IncidentViewSet)

urlpatterns = [
    path('stats/', views.StatsView.as_view()),
    path('weather/alerts/', views.WeatherAlertsView.as_view()),
    path('weather/forecast/', views.WeatherForecastView.as_view()),
    path('disasters/', views.DisastersView.as_view()),
    path('', include(router.urls)),
]
