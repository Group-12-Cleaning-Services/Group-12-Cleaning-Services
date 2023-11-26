from django.urls import path
from core.views.accounts import AccountViewset
from core.views.profile import ProfileViewset
from core.views.services import ServiceViewset
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
    #login
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #service
    path('service/all/', ServiceViewset.as_view({'get': 'list_service'})),
    path('service/create/', ServiceViewset.as_view({'post': 'create_service'})),
    path('service/update/<uuid:id>/', ServiceViewset.as_view({'post': 'update_service'})),
    path('service/delete/<uuid:id>/', ServiceViewset.as_view({'post': 'delete_service'})),
    path('service/retrieve/<uuid:id>/', ServiceViewset.as_view({'get': 'retrieve'})),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)