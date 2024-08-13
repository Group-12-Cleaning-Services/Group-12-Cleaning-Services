from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from phone_field import PhoneField


# CATEGORY = [
#     ("car", "Car Wash"),
#     ("laundry", "Laundry"),
#     ("home", "Home Cleaning")
# ]

USER_TYPE = [("customer", "Customer"), ("sales_person", "Sales")]

# SCHEDULE_STATUS = [
#     ("booked", "Booked"),
#     ("completed", "Completed"),
#     ("ongoing", "Ongoing"),
# ]


class CleaningServiceUserProfile(models.Model):
    """Cleaning Service User Profile Model"""

    profile_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contact = PhoneField(null=True, blank=True)
    profile_image = models.ImageField(upload_to="images/", blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class AccountBaseUser(BaseUserManager):
    """Cleaning Service Base User Model"""

    def create(self, email, password="1234", **extra_fields):
        if not email:
            raise ValueError("Email is required")
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        for field, value in extra_fields.items():
            setattr(user, field, value)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        user = self.model(
            email=self.normalize_email(email),
        )
        user = self.create(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class AccountUser(AbstractBaseUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    role = models.CharField(
        choices=USER_TYPE, max_length=50, default=None, null=True, blank=True
    )
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    phone = PhoneField(null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    user_image = models.ImageField(
        upload_to="images", blank=True, null=True, default=None
    )
    USERNAME_FIELD = "email"
    objects = AccountBaseUser()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        return self.email


class VerificationToken(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=50)
    time = models.DateTimeField()

    def __str__(self):
        return f"{self.email} - {self.token}"


class PasswordToken(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=50)
    time = models.DateTimeField()

    def __str__(self):
        return f"{self.email} - {self.token}"


class Medicine(models.Model):
    medicine_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=50, blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    manufacturer = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    quantity = models.DecimalField(decimal_places=2, max_digits=10)
    thumbnail = models.ImageField(
        upload_to="medicine_thumbanils/", blank=True, null=True
    )

    def __str__(self):
        return f"{self.name} - {self.category} at {self.price}"


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00, blank=True, null=True
    )
    total_price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    status = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.full_name} - {self.medicine.name} || {self.quantity} at {self.total_price}"


class Notification(models.Model):
    notification_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    user = models.ForeignKey(AccountUser, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - at notification {self.message}"


class Transaction(models.Model):
    user = models.ForeignKey(AccountUser, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    transfer_receipient_code = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.balance}"
