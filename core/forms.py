from django import forms


class ContactUsForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'name',
            'placeholder': 'نام کامل شما',
        }),
        error_messages={
            "required": "لطفا نام کامل خود را وارد کنید",
        }
    )

    email = forms.EmailField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'email',
            'placeholder': 'ایمیل شما',
        }),
        error_messages={
            "required": "لطفا ایمیل خود را وارد کنید",
            "invalid": "لطفا ایمیل معتبر وارد کنید",
        }
    )

    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'title',
            'placeholder': 'عنوان پیام',
        }),
        error_messages={
            "required": "لطفا عنوان پیام خود را وارد کنید",
        }
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'id': 'message',
            'placeholder': 'پیام شما',
            'rows': '5',
        }),
        error_messages={
            "required": "لطفا پیام خود را وارد کنید",
        }
    )
