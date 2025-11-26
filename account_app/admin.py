from django.contrib import admin
from django.utils.html import format_html
from .models import User


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'email', 'avatar_preview',
        'is_staff', 'is_active', 'is_superuser', 'date_joined', 'last_login'
    )
    list_filter = (
        'is_staff', 'is_active', 'is_superuser', 'groups', 'date_joined'
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    list_per_page = 25
    readonly_fields = ('avatar_preview', 'last_login', 'date_joined')

    fieldsets = (
        ('Authentication Info', {
            'fields': ('username', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email', 'avatar', 'avatar_preview')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="40" height="40" style="border-radius:50%;">', obj.avatar.url)
        return "No Avatar"

    avatar_preview.short_description = "Avatar"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related()
