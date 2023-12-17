"""User models admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from cride.users.models import User, Profile


class CustomUserAdmin(UserAdmin):
    """User model admin."""

    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_client', 'is_verified')
    list_filter = ('is_client', 'is_staff', 'created', 'modified')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'reputation', 'rides_taken', 'rides_offered')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    list_filter = ('reputation',)

# Así se sobreescriben modelos ya inscritos en el admin
# User ya estaba inscrito, por eso se registra así
admin.site.register(User, CustomUserAdmin)