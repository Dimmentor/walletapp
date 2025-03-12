from django.urls import path
from .views import get_balance, make_operation

urlpatterns = [
    path('api/v1/wallets/<uuid:wallet_uuid>/', get_balance, name='get_balance'),
    path('api/v1/wallets/<uuid:wallet_uuid>/operation/', make_operation, name='make_operation'),
]
