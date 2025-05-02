from users.apps import UsersConfig
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, PaymentViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register('user', UserViewSet, basename='user')
router.register('payment', PaymentViewSet, basename='payment')

urlpatterns = [

] + router.urls