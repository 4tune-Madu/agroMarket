from django.urls import path
from .views import seller_dashboard, buyer_home, admin_dashboard

urlpatterns = [
    path('seller/', seller_dashboard, name='seller_dashboard'),
    path('admin/', admin_dashboard, name='admin_dashboard'),
    path('shop/', buyer_home, name='buyer_home'),
]