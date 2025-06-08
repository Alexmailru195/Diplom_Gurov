from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import get_user_model


User = get_user_model()


# === Форма регистрации ===
class RegisterForm(forms.Form):
    """
    Форма регистрации нового пользователя.
    Проверяет:
    - Уникальность имени пользователя
    - Корректность email (формат и уникальность)
    - Совпадение паролей
    """

    username = forms.CharField(
        label='Имя пользователя',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Введите имя пользователя'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'Введите ваш email'})
    )
    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'})
    )
    password2 = forms.CharField(
        label='Подтвердите пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'})
    )

    def clean_username(self):
        """Проверка уникальности имени пользователя"""
        username = self.cleaned_data['username'].strip()
        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким именем уже существует.')
        return username

    def clean_email(self):
        """Проверка формата и уникальности email"""
        email = self.cleaned_data['email'].strip()
        validate_email(email)  # Проверка формата email
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже зарегистрирован.')
        return email

    def clean_password2(self):
        """Проверка совпадения паролей"""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Пароли не совпадают.')
        return password2

    def save(self):
        """
        Сохранение пользователя с is_active=False до подтверждения email
        """
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
            is_active=False  # пользователь не активен до верификации email
        )
        return user


# === Форма входа ===
class LoginForm(AuthenticationForm):
    """
    Форма входа в систему.
    Дополнительно проверяет, активирован ли аккаунт через email.
    """

    def confirm_login_allowed(self, user):
        """Проверяет, активирован ли аккаунт"""
        if not user.is_active:
            raise forms.ValidationError(
                "Этот аккаунт не активирован. Пожалуйста, подтвердите ваш email.",
                code='inactive'
            )
