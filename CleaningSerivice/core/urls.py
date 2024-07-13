from django.urls import path
from core.views.accounts import AccountViewset, SignIn
from core.views.profile import ProfileViewset
from core.views.medicine import MedicineViewset
from core.views.notification import NotificationViewset
from core.views.reset_password import PasswordResetViewset
from core.views.transactions import PaymentViewset, Dashboard, Withdraw
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('accounts/create/', AccountViewset.as_view({'post': 'create'})),
    path('accounts/verify-account/', AccountViewset.as_view({'post': 'verify_email'})),
    path('accounts/resend-verification-pin/', AccountViewset.as_view({'post': 'send_verification_email'})),
    #profile
    path('profile/', ProfileViewset.as_view({'get': 'list'})),
    path('profile/create/', ProfileViewset.as_view({'post': 'create'})),
    path('profile/update/', ProfileViewset.as_view({'post': 'update'})),
    path('profile/retrieve/', ProfileViewset.as_view({'get': 'retrieve'})),
    #login
    path('login/', SignIn.as_view({'post':'post'}), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #password reset
    path('accounts/password-reset/', PasswordResetViewset.as_view({'post': 'password_reset_request'})),
    path('accounts/password-reset-confirm/', PasswordResetViewset.as_view({'post': 'password_reset_confirm'})),
    #service
    path('medicine/all/', MedicineViewset.as_view({'get': 'list_service'})),
    path('medicine/providers/', MedicineViewset.as_view({'get': 'list_service_providers'})),
    path('medicine/create/', MedicineViewset.as_view({'post': 'create_service'})),
    path('medicine/update/<uuid:id>/', MedicineViewset.as_view({'post': 'update_service'})),
    path('medicine/delete/<uuid:id>/', MedicineViewset.as_view({'delete': 'delete_service'})),
    path('medicine/retrieve/<uuid:id>/', MedicineViewset.as_view({'get': 'retrieve'})),
    # path('medicine/order/', PaymentViewset.as_view({'post': 'initialize_transaction'})),
    path('medicine/order/', PaymentViewset.as_view({'post': 'verify_transaction'})),
    path('medicine/user-order/', MedicineViewset.as_view({'get': 'list_ordered_medicine_of_customer'})),
    path('medicine/service-feedback/<uuid:id>/', MedicineViewset.as_view({'post': 'service_feedback'})),
    path('medicine/provider-services/<uuid:id>/', MedicineViewset.as_view({'get':'get_service_provider_services'})),
    path('medicine/list-provider-services/', MedicineViewset.as_view({'get':'list_service_provider_services'})),
    path('medicine/list-service-provider-booked-services/', MedicineViewset.as_view({'get':'list_booked_service_of_provider'})),
    path('medicine/update-booked-service/<uuid:id>/', MedicineViewset.as_view({'post':'update_booked_service'})),
    path('service/delete-booked-service/<uuid:id>/', MedicineViewset.as_view({'delete':'cancel_booked_service'})),
    #Transaction
    path('transaction/all/', Dashboard.as_view({'get': 'get_transaction'})),
    path('transaction/transfer/', Withdraw.as_view({'post': 'initialize_transfer'})),
    ##Notification
    path('notification/all/', NotificationViewset.as_view({'get': 'list'})),
    path('notification/delete/', NotificationViewset.as_view({'delete': 'delete'})),

]
