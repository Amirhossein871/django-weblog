from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'guest_name', 'guest_email']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'نظر خودت رو بنویس...',
                'rows': 4,
            }),
            'guest_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام شما ...',
            }),
            'guest_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل شما...',
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        guest_name = cleaned_data.get('guest_name')
        guest_email = cleaned_data.get('guest_email')

        if not self.user or not self.user.is_authenticated:
            if not guest_name or not guest_email:
                raise forms.ValidationError("Please Enter your name and email")

        return cleaned_data
