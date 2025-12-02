from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


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
        'class': 'form-control input-custom',
        'placeholder': 'نام کاربری یا ایمیل خود را وارد کنید',
    }), error_messages={
        "required": "لطفاً نام کاربری خود را وارد کنید",
    }, )
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control input-custom',
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


class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control input-custom',
    }), error_messages={
        'required': 'لطفا ایمیل خود را وارد کنید',
        'invalid': 'لطفا ایمیل معتبر وارد کنید'
    })
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control input-custom'
    }), error_messages={
        'required': 'لطفا نام کاربری خود را وارد کنید',
    })

    password1 = forms.CharField(label="رمز عبور", widget=forms.PasswordInput(attrs={
        'class': 'form-control input-custom',
        'id': 'password1',
    }), error_messages={
        'required': 'لطفا رمز عبور خود را وارد کنید',
    })

    password2 = forms.CharField(label="تکرار رمز عبور", widget=forms.PasswordInput(attrs={
        'class': 'form-control input-custom',
        'id': 'password2',
    }), error_messages={
        'required': 'لطفا تکرار رمز عبور را وارد کنید',
    })

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("ایمیل وارد شده قبلاً ثبت شده")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("نام کاربری وارد شده قبلا ثبت شده است")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("رمز عبور و تکرار آن همخوانی ندارند")

        return password2


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control input-custom',
    }), error_messages={
        'required': 'لطفا ایمیل خود را وارد کنید',
        'invalid': 'لطفا ایمیل معتبر وارد کنید'
    })


class SetNewPasswordForm(forms.Form):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control input-custom"}),
        label="رمز جدید"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control input-custom"}),
        label="تکرار رمز"
    )

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password1") != cleaned.get("password2"):
            raise forms.ValidationError("رمزها یکسان نیستند!")
        return cleaned
