import uuid
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .models import Profile

User = get_user_model()


def register_view(request):
    """
    Представление для регистрации нового пользователя.
    - Проверяет форму
    - Создаёт пользователя
    - Генерирует токен
    - Отправляет письмо с подтверждением
    """

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 1. Сохраняем пользователя
            user = form.save()

            # 2. Генерируем токен и создаём профиль
            token = str(uuid.uuid4())
            Profile.objects.create(
                user=user,
                email_token=token,
                is_verified=False
            )

            # 3. Формируем ссылку и отправляем письмо
            verification_link = request.build_absolute_uri(f'/accounts/verify/{token}')
            try:
                send_mail(
                    'Подтвердите ваш email',
                    f'Для завершения регистрации перейдите по ссылке:\n{verification_link}',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                return render(request, 'accounts/register_done.html')
            except Exception as e:
                # Логирование ошибки (например, проблемы с SMTP сервером)
                messages.error(request, 'Ошибка при отправке email. Попробуйте снова.')
                return render(request, 'accounts/register.html', {'form': form})
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def verify_email(request, token):
    """
    Подтверждение email по токену.
    - Находит профиль по токену
    - Активирует пользователя
    - Перенаправляет на страницу успешного подтверждения
    """
    try:
        profile = Profile.objects.get(email_token=token)
        user = profile.user

        # Активируем пользователя
        user.is_active = True
        user.save()

        # Обновляем статус профиля
        profile.email_token = ''
        profile.is_verified = True
        profile.save()

        # Логиним пользователя после верификации
        auth_login(request, user)

        return render(request, 'accounts/verified.html')

    except Profile.DoesNotExist:
        return render(request, 'accounts/invalid_token.html')


def login_view(request):
    """
    Страница входа в систему
    """
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, 'Вы успешно вошли в систему')
            return redirect('home')  # замени 'home' на нужный маршрут
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')

    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """
    Выход из системы
    """
    auth_logout(request)
    messages.info(request, 'Вы вышли из аккаунта')
    return redirect('home')
