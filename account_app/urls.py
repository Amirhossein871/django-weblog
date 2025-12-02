from django.urls import path
from .views import (
    CustomLoginView, CustomLogoutView, RegisterView, ActivateAccountView, ForgotPasswordView, ResetPasswordView
)

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path("register/", RegisterView.as_view(), name="register"),
    path("activate/<uidb64>/<token>/", ActivateAccountView.as_view(), name="activate"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("reset-password/<uidb64>/<token>/", ResetPasswordView.as_view(), name="reset-password"),
]
