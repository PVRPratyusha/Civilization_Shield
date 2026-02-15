from django.urls import path
from . import views

urlpatterns = [
    path('', views.AnalyticsOverviewView.as_view()),
    path('forecast/disasters/', views.DisasterForecastView.as_view()),
    path('risk/area/', views.RiskScoreView.as_view()),
    path('recommend/shelter/', views.ShelterRecommendView.as_view()),
    path('anomaly/consumption/', views.AnomalyDetectView.as_view()),
]
