from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.senders.accounts import *
from core.senders.medicine import *
from core.retrievers.accounts import *
from core.retrievers.medicines import *
from core.models import Transaction
import requests
from core.utils import *
from core.serializers import TransactionSerializer
import json
import os
import threading
import time


class PaymentViewset(viewsets.ViewSet):

    def initialize_transaction(self, request):

        SECRET_KEY = os.environ.get("PAYSTACK_SECRET_KEY")
        medicine_id = request.data.get("medicine_id")
        quantity = int(request.data.get("quantity"))
        email = request.data.get("email")
        # service_time = request.data.get('time')

        url = "https://api.paystack.co/transaction/initialize"
        # print(user)
        # print(service_id)

        if email is None or medicine_id is None:
            context = {"error": "user and service id is required"}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        medicine = get_medicine_by_id(medicine_id)
        if medicine:
            data = {
                "email": email,
                "amount": str(medicine.price * quantity * 10),
                "currency": "GHS",
            }
            headers = {
                "Authorization": f"Bearer {SECRET_KEY}",
                "Content-Type": "application/json",
            }
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                data = response.json()
                verify_thread = threading.Thread(
                    target=self.verify_transaction,
                    args=[request, data["data"]["reference"]],
                )
                verify_thread.start()
                return Response(data=data, status=status.HTTP_200_OK)
            else:
                return Response(response.text, status=response.status_code)
        return Response(
            {"error": "service not found"}, status=status.HTTP_404_NOT_FOUND
        )

    def verify_transaction(self, request, reference) -> Response:
        time.sleep(60)

        SECRET_KEY = os.environ.get("PAYSTACK_SECRET_KEY")
        medicine_id = request.data.get("medicine_id")
        quantity = int(request.data.get("quantity"))
        data = request.data.copy()
        full_name = request.data.get("full_name")
        data.pop("medicine_id")
        data["quantity"] = int(data.get("quantity"))

        url = f"https://api.paystack.co/transaction/verify/{reference}"

        headers = {
            "Authorization": f"Bearer {SECRET_KEY}",
            "Content-Type": "application/json",
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response = response.json()
            if response["data"]["status"] == "success":
                medicine = get_medicine_by_id(medicine_id)
                medicine.quantity -= quantity
                medicine.save()
                data = request.data
                ordered_medicine = order_medicine(
                    medicine=medicine,
                    full_name=full_name,
                    quantity=quantity,
                    address=request.data.get("address"),
                )
                # Transaction.objects.create(user=user, balance=service.price)

                # try:
                #     service_transaction = Transaction.objects.get(user=service.user)
                #     update_provider_balance(service_transaction, service.price)
                # except:
                #     create_provider_balance(service.user, service.price)
                context = {
                    "detail": "Medicine orderered successfully",
                    "data": ordered_medicine,
                }
                return Response(context, status=status.HTTP_200_OK)
            else:
                context = {"detail": "Transaction failed"}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(response.text, status=response.status_code)


class Withdraw(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def initialize_transfer(self, request):
        amount = request.data.get("amount")
        user = get_user_from_jwttoken(request)
        url = "https://api.paystack.co/transfer"
        SECRET_KEY = os.environ.get("PAYSTACK_SECRET_KEY")
        if user is None or amount is None:
            context = {"error": "user and amount is required"}
            return Response(context, status=status.HTTP_204_NO_CONTENT)
        headers = {
            "Authorization": f"Bearer {SECRET_KEY}",
            "Content-Type": "application/json",
        }
        transaction = Transaction.objects.get(user=user)
        if transaction:
            print(transaction.balance)
            if transaction.balance < int(amount):
                context = {"detail": "Insufficient balance"}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        context = {
            "detail": "Withdrawal successful",
        }
        transaction.balance -= int(amount)
        transaction.save()
        return Response(context, status=status.HTTP_200_OK)


class Dashboard(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_transaction(self, request):

        user = get_user_from_jwttoken(request)
        transaction = Transaction.objects.filter(user=user)
        if transaction:
            serializers = TransactionSerializer(transaction, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            context = {"detail": "No transaction found"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
