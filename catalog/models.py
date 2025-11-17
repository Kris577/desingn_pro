from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = models.CharField(max_length=50, verbose_name='Имя', blank=False)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия', blank=False)
    patronymic = models.CharField(max_length=50, verbose_name='Отчество', blank=False)
    username = models.CharField(max_length=200, verbose_name='Логин', unique=True, blank=False)
    email = models.CharField(max_length=254, verbose_name='Почта', unique=True, blank=False)
    password = models.CharField(max_length=254, verbose_name='Пароль', blank=False)
    date_of_birth = models.DateField(verbose_name='Дата рождения', blank=False, default='2007-01-01')

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.first_name
