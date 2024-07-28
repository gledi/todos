from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, Activation


@admin.register(Activation)
class ActivationAdmin(admin.ModelAdmin):
    list_display = ('user', 'activation_key', 'is_used', 'created_at', 'updated_at')
    list_filter = ('is_used',)
    search_fields = ('user__username', 'activation_key')
    ordering = ('-created_at',)


@admin.register(User)
class UserAdmin(_UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "phone")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
