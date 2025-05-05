from django.contrib.auth.admin import UserAdmin
from .models import Users
from django.contrib import admin

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = Users
    list_display = ("email", "phone", "name", "created_at", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password", "name", "phone")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff", "name", "phone",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    
    
admin.site.register(Users, CustomUserAdmin)