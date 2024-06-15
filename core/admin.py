from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Tag, Ingredient

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['id', 'name', 'email']
    ordering = ['id']
    fieldsets = (
            (None, {"fields": ("email", "password")}),
            (_("Personal info"), {"fields": ("name",)}),
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
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

admin.site.register(Tag)
admin.site.register(Ingredient)