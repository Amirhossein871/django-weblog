from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm
from django.contrib import messages


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
