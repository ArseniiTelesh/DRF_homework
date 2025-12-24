from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import LinkValidator


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = ['user']


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LinkValidator(field="material_link")]

class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """Определяет, подписан ли текущий пользователь на этот курс"""
        user = self.context.get('request').user

        # Если пользователь не авторизован
        if not user or user.is_anonymous:
            return False

        # Проверяем, есть ли активная подписка пользователя на этот курс
        return Subscription.objects.filter(
            user=user,
            course=obj,
            is_active=True
        ).exists()
