from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer


#########################################################
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny, )

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

#########################################################
class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['payment_date']