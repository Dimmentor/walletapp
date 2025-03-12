from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Wallet
import uuid


class WalletTests(APITestCase):
    def setUp(self):
        self.wallet_uuid = uuid.uuid4()
        self.wallet = Wallet.objects.create(uuid=self.wallet_uuid, balance=1000)

    def test_get_balance(self):
        path = reverse('get_balance', args=[self.wallet_uuid])
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['balance'], '1000.00')

    def test_deposit_operation(self):
        path = reverse('make_operation', args=[self.wallet_uuid])
        data = {
            'operation_type': 'DEPOSIT',
            'amount': 500
        }
        response = self.client.post(path, data, format='json')
        self.wallet.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['balance']), '1500.00')

    def test_withdraw_operation(self):
        path = reverse('make_operation', args=[self.wallet_uuid])
        data = {
            'operation_type': 'WITHDRAW',
            'amount': 200
        }
        response = self.client.post(path, data, format='json')
        self.wallet.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['balance']), '800.00')

    def test_withdraw_wrong_amount(self):
        path = reverse('make_operation', args=[self.wallet_uuid])
        data = {
            'operation_type': 'WITHDRAW',
            'amount': 2000
        }
        response = self.client.post(path, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
