from django.db import models


# Create your models here.

class ContactUsModel(models.Model):
    class Meta:
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'
        ordering = ['-created_at']

    name = models.CharField(max_length=255, verbose_name="Name")
    email = models.EmailField(max_length=255, verbose_name="Email")
    title = models.CharField(max_length=255, verbose_name='Title')
    message = models.TextField(verbose_name='Message')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")

    def __str__(self):
        return f"{self.email};"
