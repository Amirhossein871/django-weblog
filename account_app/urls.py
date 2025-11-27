from django.urls import path
from .views import (
    CustomLoginView, CustomLogoutView, RegisterView, ActivateAccountView
)

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path("register/", RegisterView.as_view(), name="register"),
    path("activate/<uidb64>/<token>/", ActivateAccountView.as_view(), name="activate"),
]
