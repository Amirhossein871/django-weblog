from django.urls import path
from .views import about_us, contact_us

urlpatterns = [
    path('about-us/', about_us, name='about-us'),
    path('contact-us/', contact_us, name='contact-us'),
]
