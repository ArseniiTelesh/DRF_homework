from rest_framework import serializers

from materials.serializers import CourseSerializer, LessonSerializer
from users.models import User, Payment


class UserSerializer(serializers.ModelSerializer):
    payments = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "email", "password", "phone_number", "city", "payments", "is_active", "is_staff", "is_superuser")

    def get_payments(self, obj):
        payments = obj.payment_set.all()
        return PaymentSerializer(payments, many=True).data


class PaymentSerializer(serializers.ModelSerializer):
    paid_course = CourseSerializer(read_only=True)
    paid_lesson = LessonSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "phone_number", "city", "avatar", "is_active")


class PrivateUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ("id",  "email", "password", "phone_number", "city", "avatar",
                 "payments", "is_active", "is_staff", "is_superuser")