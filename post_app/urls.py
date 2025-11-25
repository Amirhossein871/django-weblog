from django.urls import path
from .views import index, post_detail, toggle_like, toggle_save

urlpatterns = [
    path('', index, name='index'),
    path('post/<slug:slug>/', post_detail, name='post_detail'),
    path('post/<slug:slug>/toggle_like/', toggle_like, name='toggle_like'),
    path('post/<slug:slug>/toggle_save/', toggle_save, name='toggle_save'),
]
