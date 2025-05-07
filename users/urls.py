from django.urls import path
from rest_framework.permissions import AllowAny

from users.apps import UsersConfig
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, PaymentViewSet, UserCreateAPIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
app_name = UsersConfig.name

router = DefaultRouter()
router.register('user', UserViewSet, basename='user')
router.register('payment', PaymentViewSet, basename='payment')

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny, )), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny, )), name='token_refresh'),

] + router.urls