"""
admin_user.py
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.models.user import User


@admin.register(User)
class AdminUser(UserAdmin):
    """
    @admin.register(User)
    class AdminUser(UserAdmin)
    """

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        disabled_fields = set()

        if not request.user.is_superuser:
            disabled_fields.update({"is_staff", "is_superuser"})

        if obj is not None:
            disabled_fields.update({"email"})

        for field in disabled_fields:
            if field in form.base_fields:
                form.base_fields[field].disabled = True

        return form

    model = User
    list_display = ("email", "is_active", "is_staff", "is_superuser", "last_login", "date_joined", )
    list_filter = ("email", "is_active", "is_staff", "is_superuser", )
    readonly_fields = ("last_login", "date_joined", )
    fieldsets = (
        (None, {
            "fields": ("email", "password", ),
            }),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser", ),
            }),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide", ),
            "fields": ("email", "password1", "password2", "is_staff", "is_active", )
            }),
    )
    search_fields = ("email", )
    ordering = ("email", )
