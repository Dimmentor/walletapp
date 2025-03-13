from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Wallet
from .serializers import WalletSerializer, OperationSerializer
from .utils import retry_operation


def create_wallet(wallet_uuid):
    return Wallet.objects.create(uuid=wallet_uuid)


@api_view(['POST'])
def make_operation(request, wallet_uuid):
    wallet = Wallet.objects.filter(uuid=wallet_uuid).first()
    if wallet is None:
        wallet = create_wallet(wallet_uuid)

    serializer = OperationSerializer(data=request.data)
    if serializer.is_valid():
        operation_type = serializer.validated_data['operation_type']
        amount = serializer.validated_data['amount']

        try:
            if operation_type == 'DEPOSIT':
                retry_operation(wallet, amount)
            elif operation_type == 'WITHDRAW':
                if wallet.balance >= amount:
                    retry_operation(wallet, -amount)
                else:
                    return Response({"message": "Недостаточно средств."}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"balance": wallet.balance}, status=status.HTTP_200_OK)

        except Wallet.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_balance(request, wallet_uuid):
    try:
        wallet = Wallet.objects.get(uuid=wallet_uuid)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)
    except Wallet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
