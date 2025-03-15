from django.db import IntegrityError


def retry_operation(wallet, amount, retries=3):
    for attempt in range(retries):
        try:
            wallet.update_balance(amount)
            return True
        except IntegrityError:
            wallet.refresh_from_db()
    return False
