from core.models import *
from rest_framework import serializers
import bleach


class BleachSerializer(serializers.ModelSerializer):
    """Serializer that applies bleach.clean to string fields"""

    def to_internal_value(self, data):
        cleaned_data = super().to_internal_value(data)

        for field_name, field_value in cleaned_data.items():
            if isinstance(field_value, str):
                cleaned_data[field_name] = bleach.clean(field_value, strip=True)

        return cleaned_data


class CleaningServiceUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CleaningServiceUserProfile
        fields = [
            "profile_id",
            "first_name",
            "last_name",
            "contact",
            "profile_image",
            "time_created",
        ]


class AccountUserSerializer(BleachSerializer):
    class Meta:
        model = AccountUser
        fields = ["user_id", "email", "role", "full_name", "phone", "user_image"]
        extra_kwargs = {
            "password": {"write_only": True},
            "is_active": {"read_only": True},
            "is_staff": {"read_only": True},
            "is_superuser": {"read_only": True},
        }


class VerificationTokenSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"


class PasswordTokenSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """Category Serializer"""

    class Meta:
        model = Category
        fields = "__all__"


class MedicineSerializer(serializers.ModelSerializer):
    """Medicine Serializer"""

    class Meta:
        model = Medicine
        fields = [
            "medicine_id",
            "name",
            "category",
            "price",
            "quantity",
            "description",
            "manufacturer",
            "thumbnail",
        ]


class OrderSerializer(serializers.ModelSerializer):
    """Order Serializer"""

    medicine = MedicineSerializer()

    class Meta:
        model = Order
        fields = [
            "order_id",
            "medicine",
            "quantity",
            "status",
            "full_name",
            "address",
            "created_at",
        ]


class TransactionSerializer(serializers.ModelSerializer):
    """Transaction Serializer"""

    class Meta:
        model = Transaction
        fields = "__all__"
        extra_kwargs = {
            "balance": {
                "min_value": 0.00,
            }
        }


class NotificationSerializer(serializers.ModelSerializer):
    """Notification Serializer"""

    user = AccountUserSerializer()

    class Meta:
        model = Notification
        fields = "__all__"
        extra_kwargs = {
            "read": {
                "default": False,
            }
        }
