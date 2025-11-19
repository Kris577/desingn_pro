from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator
from datetime import date
from .models import User, Application, Category


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(
        label="Имя",
        validators=[
            RegexValidator(
                regex=r'^[А-яЁё -]+$',
                message="Имя должно содержать только кириллические буквы, дефисы и пробелы"
            )
        ]
    )
    last_name = forms.CharField(
        label="Фамилия",
        validators=[
            RegexValidator(
                regex=r'^[А-яЁё -]+$',
                message="Фамилия должна содержать только кириллические буквы, дефисы и пробелы"
            )
        ]
    )
    patronymic = forms.CharField(
        label="Отчество",
        validators=[
            RegexValidator(
                regex=r'^[А-яЁё -]+$',
                message="Отчество должно содержать только кириллические буквы, дефисы и пробелы"
            )
        ]
    )
    username = forms.CharField(
        label="Логин",
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9-]+$',
                message="Логин должен содержать только латиницу и дефисы"
            )
        ]
    )
    email = forms.EmailField(
        label="Почта",
        validators=[EmailValidator(message="Введите действительный email-адрес")]
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput
    )

    consent = forms.BooleanField(
        label="Согласие на обработку персональных данных",
        error_messages={"required": "Необходимо согласие на обработку персональных данных"}
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Логин уже занят")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Такая почта уже зарегестрирована")
        return email

    def clean(self):
        super().clean()

        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            self.add_error("password2", "Пароли должны совпадать")

        return self.cleaned_data

    def save(self, commit=True):
        new_user = super().save(commit=False)
        new_user.set_password(self.cleaned_data.get("password"))
        if commit:
            new_user.save()
        return new_user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'patronymic', 'username', 'email')

class ApplicationForm(forms.ModelForm):
    title = forms.CharField(
        label="Название заявки",
        max_length=200,
    )

    description = forms.CharField(
        label="Описание",
        widget=forms.Textarea,
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select,
        label="Категория",
        help_text="Выберите категорию."
    )

    image = forms.ImageField(
        label="Изображение",
    )

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.status = 'new'
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Application
        fields = ['title', 'description', 'category', 'image']