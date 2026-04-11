from django.urls import path
from .views import seller_dashboard

urlpatterns = [
    path('seller/', seller_dashboard, name='seller_dashboard'),
]