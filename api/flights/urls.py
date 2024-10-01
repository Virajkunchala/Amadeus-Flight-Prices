from django.urls import path
from .views import FlightOffersView,Pingview,HealthCheckView


urlpatterns = [
    path('flights/ping/', Pingview.as_view(), name='ping'),
    path('flights/price/', FlightOffersView.as_view(), name='flight-price'),
    path('flights/health/', HealthCheckView.as_view(), name='health-check'),
    
]