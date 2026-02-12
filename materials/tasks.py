from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from datetime import timedelta

from materials.models import Course, Subscription
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def send_course_update_notification(course_id):
    """
    Отправляет уведомления подписчикам об обновлении курса
    """
    course = Course.objects.get(id=course_id)

    # Находим всех активных подписчиков этого курса
    subscriptions = Subscription.objects.filter(
            course=course,
            is_active=True
        ).select_related('user')

    # Собираем email адреса подписчиков
    emails = [sub.user.email for sub in subscriptions if sub.user and sub.user.email]

    if emails:
        subject = f'Обновление курса: {course.title}'
        message = f'''
        Здравствуйте!
        Курс "{course.title}" был обновлен.
        Проверьте новые материалы по ссылке: 
        http://localhost:8000/materials/courses/{course.id}/

        С уважением,
        Команда образовательной платформы
        '''

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=emails,
            fail_silently=False,
        )

        print(f"Уведомления отправлены {len(emails)} подписчикам курса '{course.title}'")

    print(f"Нет активных подписчиков для курса '{course.title}'")


@shared_task
def check_last_login():
    """Проверка последнего входа пользователей и отключение неактивных пользователей"""
    users = User.objects.filter(last_login__isnull=False)
    today = timezone.now()
    for user in users:
        if today - user.last_login > timedelta(days=30):
            user.is_active = False
            user.save()
            print(f'Пользователь {user.email} отключен')
        else:
            print(f'Пользователь {user.email} активен')