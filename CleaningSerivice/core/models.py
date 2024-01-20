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

USER_TYPE = [
    ("customer", "Customer"),
    ("service_provider", "Service Provider")
]

SCHEDULE_STATUS = [
    ("booked", "Booked"),
    ("completed", "Completed"),
    ("ongoing", "Ongoing"),
]

class CleaningServiceUserProfile(models.Model):
    """Cleaning Service User Profile Model"""
    profile_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contact = PhoneField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='images/', blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.first_name + " " + self.last_name


class CleaningServiceBaseUser(BaseUserManager):
    """Cleaning Service Base User Model"""
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        user = self.model(
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        user = self.model(
            email = self.normalize_email(email),
        )
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)   
        return user     
        

class CleaningServiceUser(AbstractBaseUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.OneToOneField(CleaningServiceUserProfile, on_delete=models.CASCADE, related_name='profile', null=True, blank=True)
    email = models.EmailField(unique=True)
    user_type = models.CharField(choices=USER_TYPE, max_length=50, default=None, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    organization_name = models.CharField(max_length=255, null=True, blank=True)
    organization_logo = models.ImageField(upload_to='images', blank=True, null=True)
    USERNAME_FIELD = 'email'
    objects = CleaningServiceBaseUser()
    
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
    
    
class Service(models.Model):
    service_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=50)
    user = models.ForeignKey(CleaningServiceUser, on_delete=models.CASCADE)
    thumnail = models.ImageField(upload_to="images", blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.title} - {self.category} || {self.user.email} at {self.price}"
    

# class ServiceProvider(models.Model):
#     serviceprovider_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.OneToOneField(CleaningServiceUser, on_delete=models.CASCADE, related_name='service_provider')
#     thumnails = models.ImageField(upload_to="service_provider_thumnails", blank=True, null=True)
#     service = models.ManyToManyField(Service, related_name='service')
#     def __str__(self):
#         return f"{self.user.email} - {self.service.count()}"
    

class ScheduleService(models.Model):
    scheduleservice_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    time = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    customer = models.ForeignKey(CleaningServiceUser, on_delete=models.CASCADE)
    status = models.CharField(choices=SCHEDULE_STATUS, max_length=50, default="booked", null=True, blank=True)
    address = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.service.title} is booked by - {self.customer.email} at {self.time}"
    

class ServiceFeedback(models.Model):
    serviceFeedback_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.ForeignKey(ScheduleService, on_delete=models.CASCADE, related_name='feedback')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(default=None, null=True, blank=True)

    def __str__(self):
        return f"Feedback for {self.service.service.title} by {self.service.customer.email}"
    

class Notification(models.Model):
    notification_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CleaningServiceUser, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.email} - at notification {self.message}"


class Transaction(models.Model):
    user = models.ForeignKey(CleaningServiceUser, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    transfer_receipient_code = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.balance}"