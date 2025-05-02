from rest_framework import serializers

from materials.serializers import CourseSerializer, LessonSerializer
from users.models import User, Payment


class UserSerializer(serializers.ModelSerializer):
    payments = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_payments(self, obj):
        payments = obj.payment_set.all()
        return PaymentSerializer(payments, many=True).data


class PaymentSerializer(serializers.ModelSerializer):
    paid_course = CourseSerializer(read_only=True)
    paid_lesson = LessonSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'