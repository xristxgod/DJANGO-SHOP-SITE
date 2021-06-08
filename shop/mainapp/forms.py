from django import forms
from django.contrib.auth.models import User

from .models import Order


class OrderForm(forms.ModelForm):

    ''' Форма для оформления заказа '''

    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_date'].lable = 'Дата доставки'

    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'phone', 'address', 'buying_type', 'order_date', 'comment'
        ]

class LoginForm(forms.ModelForm):

    ''' Форма входа на сайт '''

    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].lable = 'Логин'
        self.fields['password'].lable = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Пользователь с логином {username} не найдене в системе')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Неверный пароль')
        return self.cleaned_data

    class Meta:
        model = User
        fields = [
            'username', 'password'
        ]

class RegistrationForm(forms.ModelForm):

    ''' Форма регистрации '''

    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(required=False)
    address = forms.CharField(required=False)
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].lable = 'Логин'
        self.fields['first_name'].lable = 'Имя'
        self.fields['last_name'].lable = 'Фамилия'
        self.fields['password'].lable = 'Пароль'
        self.fields['confirm_password'].lable = 'Подтвердите пароль'
        self.fields['phone'].lable = 'Номер телефона'
        self.fields['address'].lable = 'Адрес'
        self.fields['email'].lable = 'Электронная почта'

    def clean_email(self):

        ''' Проверка Email '''

        email = self.cleaned_data['email']
        domain = email.split('.')[-1]
        if domain in ['com', 'net']:
            # Если в Email домен кончается на '.com', '.net' то регестрация будет невозможна
            raise forms.ValidationError(f'Регистрация для домена "{domain}" невозможно')

        if User.objects.filter(email=email).exists():
            # Если пользователь с данным Email уже есть в системе то регестрация будет невозможна
            raise forms.ValidationError(f'Пользователь с данным {email} уже существует')
        return email

    def clean_username(self):

        ''' Проверка username '''

        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            # Если пользователь с данным username уже есть в системе то выдаст ошибку
            raise forms.ValidationError(f'Пользователь "{username}" уже есть в системе')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            # Если password не совпадает с confirm_password то будет ошибка
            raise forms.ValidationError('Пароль введен не правильно')
        return self.cleaned_data

    class Meta:
        model = User
        fields = [
            'username', 'first_name',
            'last_name', 'password',
            'confirm_password', 'phone',
            'address', 'email'
        ]

