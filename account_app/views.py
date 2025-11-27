from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm, RegisterForm
from django.contrib import messages
from django.views.generic import FormView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import Http404
from django.views import View
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your views here.

class CustomLoginView(LoginView):
    template_name = "account_app/login.html"
    form_class = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        remember = form.cleaned_data.get("remember_me")

        if not remember:
            self.request.session.set_expiry(0)
        else:
            self.request.session.set_expiry(60 * 60 * 24 * 7)

        messages.success(self.request, "ورود به حساب با موفقیت انجام شد")

        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, 'با موفقیت خارج شدید.')
        return super().dispatch(request, *args, **kwargs)


class RegisterView(FormView):
    template_name = "account_app/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect("home")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = self.request.build_absolute_uri(
            reverse_lazy("activate", kwargs={"uidb64": uid, "token": token})
        )

        send_mail(
            subject="فعال‌سازی حساب کاربری",
            message=f"{activation_link}",
            from_email="no-reply@example.com",
            recipient_list=[user.email],
        )

        messages.success(
            self.request,
            "ثبت‌نام انجام شد! لطفاً برای فعال‌سازی حساب خود ایمیل خود را بررسی کنید"
        )

        return super().form_valid(form)


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            messages.success(request, "اکانت شما با موفقیت فعال شد")
            return redirect("login")

        raise Http404()
