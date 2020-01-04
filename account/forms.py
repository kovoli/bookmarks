from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        """
        Вы можете применить метод clean_<fieldname>() к любому из полей формы,
        чтобы очистить его или проверить форму на ошибки для определенного поля.
        Формы также включают общий метод clean() - для проверки всей формы, он полезен для проверки полей,
        которые зависят друг от друга.
        """
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords dont match.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    """
    UserEditForm: Позволит пользователям редактировать свое имя, фамилию и адрес электронной почты, которые
    являются атрибутами встроенной пользовательской модели Django.
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    """
    ProfileEditForm: Позволит пользователям редактировать данные профиля,
    которые мы сохраняем в пользовательской модели Profile.
    Пользователи смогут отредактировать дату рождения и загрузить изображение для своего профиля.
    """
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')

class LoginForm(forms.Form):
    username = forms.CharField()
    # виджет PasswordInput чтобы отображать HTML-код
    # элемента input, включающего атрибут type="password", так что браузер рассматривает его как поле для ввода пароля
    password = forms.CharField(widget=forms.PasswordInput)


