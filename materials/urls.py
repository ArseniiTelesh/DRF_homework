from django.urls import path

from materials.apps import MaterialsConfig
from rest_framework.routers import DefaultRouter

from materials.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, SubscriptionAPIView, SubscriptionListAPIView

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register('courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>', LessonRetrieveAPIView.as_view(), name='lesson-get'),
    path('lesson/create', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/update/<int:pk>', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/delete/<int:pk>', LessonDestroyAPIView.as_view(), name='lesson-delete'),

    path('subscription/', SubscriptionListAPIView.as_view(), name='subscription_list'),
    path('subscription/create/', SubscriptionAPIView.as_view(), name='subscription_create'),
] + router.urls
