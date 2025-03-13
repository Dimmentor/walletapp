from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Wallet



class WalletTests(APITestCase):
    def setUp(self):
        self.wallet_uuid = '2560a9c2-588b-4a8f-b75c-37128a50af4a'
        self.wallet = Wallet.objects.create(uuid=self.wallet_uuid, balance=0)
    def test_deposit(self):
        url = reverse('make_operation', args=[self.wallet_uuid])
        data = {
            'operation_type': 'DEPOSIT',
            'amount': 100.00
        }
        response = self.client.post(url, data)
        self.wallet.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.wallet.balance, 100.00)

    def test_withdraw(self):
        self.wallet.balance = 200.00
        self.wallet.save()

        url = reverse('make_operation', args=[self.wallet_uuid])
        data = {
            'operation_type': 'WITHDRAW',
            'amount': 100.00
        }
        response = self.client.post(url, data)
        self.wallet.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.wallet.balance, 100.00)

    def test_withdraw_wrong_amount(self):
        url = reverse('make_operation', args=[self.wallet_uuid])
        data = {
            'operation_type': 'WITHDRAW',
            'amount': 100.00
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Недостаточно средств.", response.data['message'])

    def test_multiprocessing(self):
        url = reverse('make_operation', args=[self.wallet_uuid])
        data = {
            'operation_type': 'DEPOSIT',
            'amount': 50.00
        }

        responses = [self.client.post(url, data) for _ in range(10)]

        for response in responses:
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, 500.00)

    def test_version_conflict_handling(self):
        url = reverse('make_operation', args=[self.wallet_uuid])

        self.wallet.balance = 200.00
        self.wallet.save()

        response_a = self.client.post(url, {'operation_type': 'DEPOSIT', 'amount': 100.00})
        response_b = self.client.post(url, {'operation_type': 'DEPOSIT', 'amount': 150.00})

        self.assertEqual(response_a.status_code, status.HTTP_200_OK)
        self.assertEqual(response_b.status_code, status.HTTP_200_OK)

        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, 450.00)