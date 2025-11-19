from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class User(AbstractUser):
    first_name = models.CharField(verbose_name='Имя', blank=False)
    last_name = models.CharField(verbose_name='Фамилия', blank=False)
    patronymic = models.CharField(verbose_name='Отчество', blank=False)
    username = models.CharField(verbose_name='Логин', unique=True, blank=False)
    email = models.CharField(verbose_name='Почта', unique=True, blank=False)
    password = models.CharField(verbose_name='Пароль', blank=False)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.first_name

class Category(models.Model):

    name = models.CharField(help_text="Выберите категорию")

    def __str__(self):
        return self.name

def validate_image(image):
    valid_mime_types = ['image/jpeg', 'image/png', 'image/bmp']
    mime_type = image.file.content_type
    if mime_type not in valid_mime_types:
        raise ValidationError("Формат файла должен быть: jpg, jpeg, png, bmp.")

    file_size = image.size
    if file_size > 2 * 1024 * 1024:
        raise ValidationError("Размер файла не должен превышать 2 МБ.")

class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Принято в работу'),
        ('completed', 'Выполнено'),
    ]

    title = models.CharField(verbose_name="Название")
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='applications/', validators=[validate_image])
    status = models.CharField(choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
