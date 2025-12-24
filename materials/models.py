from django.conf import settings
from django.db import models
from django.db.models import URLField

NULLABLE = {"blank": True, "null": True}

class Course(models.Model):
    title = models.CharField(max_length=300, verbose_name='Название курса')
    picture = models.ImageField(upload_to='courses/previews/', verbose_name='Превью (обложка)', **NULLABLE)
    description = models.TextField(verbose_name='Описание курса', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="course_owner",
                              verbose_name="Владелец", **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=300, verbose_name='Название урока')
    description = models.TextField(verbose_name='Описание урока', **NULLABLE)
    picture = models.ImageField(upload_to='lessons/previews/', verbose_name='Превью (обложка)', **NULLABLE)
    material_link = URLField(verbose_name='Ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="lesson_owner",
                              verbose_name="Владелец", **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="subscription_user",
                              verbose_name="пользователь", **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course", verbose_name="Курс")
    is_active = models.BooleanField(default=False, verbose_name='Подписка активна')

    def __str__(self):
        return f"{self.user} подписан на {self.course}"

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        # Уникальность пары пользователь-курс
        unique_together = ['user', 'course']
