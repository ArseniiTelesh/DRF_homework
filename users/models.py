from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

NULLABLE = {"blank": True, "null": True}

class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='почта')
    phone_number = PhoneNumberField('Номер телефона', **NULLABLE)
    city = models.CharField(max_length=150, verbose_name='Город', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)

    # token = models.CharField(max_length=100, verbose_name='Token', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
