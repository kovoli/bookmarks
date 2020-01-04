from django.shortcuts import render
from django.http import HttpResponse
# Фреймворк аутентификации расположены по адресу django.contrib.auth
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile

def index(request):
    a = 'Hello World'
    return HttpResponse(a)

@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
        # Создаю нового пользователя но пока не сохраняю его
            new_user = user_form.save(commit=False)
            # Установить выбранный пароль
            """
            Вместо сохранения сырого пароля, введенного пользователем, мы используем метод set_password().
            Это метод пользовательской модели, который применяет шифрование к 
            паролю для его хранения в безопасном виде. 
            """
            new_user.set_password(user_form.cleaned_data['password'])
            # Сохранить объект User
            new_user.save()
            # Создать профиль пользователя
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    """
    Мы используем декоратор login_required потому что пользователи должны пройти аутентификацию
    для редактирования своего профиля. В этом случае мы используем две формы модели: UserEditForm для хранения
    данных встроенной пользовательской модели и ProfileEditForm для хранения дополнительных данных профиля в
    пользовательской модели Profile. Чтобы проверить предоставленные данные,
    мы выполним метод is_valid() для обоих форм. Если обе формы содержат достоверные данные,
    мы сохраним обе формы, вызвав метод save(), чтобы обновить соответствующие объекты в базе данных.
    """
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/edit.html', {'user_form': user_form,
                                                     'profile_form': profile_form})


def user_login(request):   # Запрос GET создает форму логина
    """
    Обратите внимание на разницу между authenticate и login: authenticate() проверяет учетные данные пользователя
    и возвращает объект User, если они правильны; login() создает сессию для пользователя.
    """
    if request.method == 'POST':  # пользователь отправляет форму через POST

        form = LoginForm(request.POST)  # Создаем форму с предоставленными данными
        print('Blank Form', form)
        if form.is_valid():
            # Проверяем, действительна ли форма
            # Если это не так, мы отображаем ошибки формы в нашем шаблоне
            cd = form.cleaned_data
            print('cd variable:', cd)
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            # authenticate(). Этот метод берет из объекта request параметры username, password и возвращает User
            print('user variable:', user)
            if user is not None:  # Если пользователь существует
                if user.is_active:  # Если пользователь активен
                    login(request, user)
                    # Если пользователь активен, мы регистрируем пользователя на веб-сайте.
                    # Мы создаем сессию пользователя, вызывая метод login() и возвращаем сообщение:
                    # Authenticated successfully
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})
