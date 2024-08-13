from core.models import *
from core.serializers import MedicineSerializer, OrderSerializer, CategorySerializer
from core.retrievers.medicines import *
from core.models import AccountUser  # Import the AccountUser type

import json


def create_medicine(data, files) -> dict:
    """create medicine"""
    # data = data.dict()
    # data['doctor'] = {'user_id': user.user_id}
    # medicine = Medicine.objects.create(**data)
    serializer = MedicineSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    return serializer.errors


def update_medicine(medicine, data):
    """Update a medicine

    Args:
        data (str):  post data to the with the required serive
        medicine (Service): Service instance
        Return a serialized dict
    """
    serializer = MedicineSerializer(instance=medicine, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    else:
        return None


def send_all_medicines():
    """Get all medicines from the database"""
    medicines_queryset = get_all_medicine()

    serializer = MedicineSerializer(medicines_queryset, many=True)

    return serializer.data


def send_all_medicines_by_category(category: str):
    """Get all medicines by category

    Args:
        category (str): category of the medicine
    """
    medicines_queryset = get_medicine_by_category(category)
    serializer = MedicineSerializer(medicines_queryset, many=True)
    return serializer.data


def order_medicine(full_name, medicine, quantity, address) -> dict:
    """Book a medicine

    Args:
        medicine (Service): Service instance
        user (AccountUser): AccountUser instance
        data (str): post data with required fields
    """
    medicine = Order.objects.create(
        medicine=medicine, full_name=full_name, quantity=quantity, address=address
    )
    # for kwarg in data:
    #     if hasattr(medicine, kwarg):
    #         setattr(medicine, kwarg, data[kwarg])
    medicine.paid = True
    medicine.save()
    serializer = OrderSerializer(medicine).data
    return serializer


def get_order_by_id(order_id):
    """Get order by id

    Args:
        order_id (str): order id
    """
    try:
        order = Order.objects.get(order_id=order_id)
    except Order.DoesNotExist:
        return None
    return order


def send_all_booked_medicine() -> dict:
    """Get all booked medicine

    Return: All booked medicine
    """
    ordered_medicine_queryset = get_all_booked_medicine()
    serializer = OrderSerializer(ordered_medicine_queryset, many=True)
    return serializer.data


def send_booked_medicine_by_customer(customer: AccountUser) -> dict:
    """Get all booked medicine by a customer

    Args:
        customer (AccountUser): CleaningServiceUser instance
        Return: All booked medicine by a customer
    """
    ordered_medicine_queryset = get_ordered_medicine_by_customer(customer)
    serializer = OrderSerializer(ordered_medicine_queryset, many=True)
    print(serializer.data)
    return serializer.data


def send_ordered_medicine_by_docter(provider: AccountUser) -> dict:
    """Get all booked medicine by a provider

    Args:
        provider (CleaningServiceUser): CleaningServiceUser instance
        Return: All booked medicine by a provider
    """
    ordered_medicine_queryset = get_ordered_medicine_by_doctor(provider)
    serializer = OrderSerializer(ordered_medicine_queryset, many=True)
    return serializer.data


def create_category(data) -> dict:
    serializer = CategorySerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    else:
        return serializer.errors


def update_category(category: Category, data) -> dict:
    serializer = CategorySerializer(instance=category, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    else:
        return serializer.errors


def create_feedback(review: str, medicine: Order, rating: str) -> dict:
    """Create feedback

    Args:
        data (str): post data with required fields
    """
    medicine_feedback = ServiceFeedback.objects.create(
        medicine=medicine, rating=rating, review=review
    )
    serializer = ServiceFeedbackSerialiazer(medicine_feedback)
    return serializer.data


def all_profiles():
    """Get all profiles"""
    queryset = CleaningServiceUserProfile.objects.all()
    serializer = CleaningServiceUserProfileSerializer(queryset, many=True)
    return serializer.data


def create_provider_balance(user, amount):
    """Create provider balance

    Args:
        user (CleaningServiceUser): CleaningServiceUser instance
        amount (int): amount to be added to the balance

    Returns:
        Transaction: Transaction instance
    """
    transaction = Transaction.objects.create(user=user, balance=amount)
    return transaction

    # def update_provider_balance(transaction:Transaction, amount):
    """ Update provider balance

    Args:
        Transaction (Transation): Transaction instance
        amount (int): amount to be added to the balance

    Returns:
        Transaction: Transaction instance
    """
    transaction.balance += amount
    transaction.save()
    return transaction


def create_category(data) -> dict:
    serializer = CategorySerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    else:
        return None


def update_category(category: Category, data) -> dict:
    serializer = CategorySerializer(instance=category, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    else:
        return None
