from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    error_messages = {
        "invalid_login": (
            "نام کاربری یا رمز عبور اشتباه است لطفا دوباره تلاش کنید."
        ),
        "inactive": (
            "حساب شما غیرفعال است. لطفاً ابتدا حساب خود را فعال کنید یا در صورت مشکل با پشتیابی تماس بگیرید."
        ),
    }

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'نام کاربری یا ایمیل خود را وارد کنید',
    }), error_messages={
        "required": "لطفاً نام کاربری خود را وارد کنید",
    }, )
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'رمز عبور خود را وارد کنید',
    }), error_messages={
        "required": "لطفاً رمز عبور رو وارد کن!",
    }, )
    remember_me = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        })
    )