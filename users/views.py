from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.permissions import IsProfileOwner
from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer, PublicUserSerializer, PrivateUserSerializer
from users.services import convert_currency, create_stripe_price, create_stripe_session


#########################################################
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            if self.request.user != self.get_object():
                return PublicUserSerializer
            return PrivateUserSerializer
        elif self.action in ['update', 'partial_update']:
            return PrivateUserSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsProfileOwner]
        return super().get_permissions()


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


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        amount_in_dollars = convert_currency(payment.amount)
        price = create_stripe_price(amount_in_dollars)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link_payment = payment_link
        payment.save()