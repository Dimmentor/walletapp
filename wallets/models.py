from django.db import models
from django.db import transaction


class Wallet(models.Model):
    uuid = models.UUIDField(primary_key=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['uuid'], name='unique_wallet_uuid')
        ]

    def update_balance(self, amount):
        with transaction.atomic():
            self.balance += amount
            self.save()