from django.db import models
from django.db.models import URLField

NULLABLE = {"blank": True, "null": True}

class Course(models.Model):
    title = models.CharField(max_length=300, verbose_name='Название курса')
    picture = models.ImageField(upload_to='courses/previews/', verbose_name='Превью (обложка)', **NULLABLE)
    description = models.TextField(verbose_name='Описание курса', **NULLABLE)


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


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
