from django.urls import path
from .views import make_operation, get_balance

urlpatterns = [
    path('api/v1/wallets/<uuid:wallet_uuid>/operation', make_operation, name='make_operation'),
    path('api/v1/wallets/<uuid:wallet_uuid>/', get_balance, name='get_balance'),
]