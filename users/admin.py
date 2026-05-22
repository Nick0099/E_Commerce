from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email','name', 'is_seller', 'is_staff', 'created_at')
    list_filter = ('is_seller', 'is_staff', 'is_active')
    search_fields = ('email', 'name')
    ordering= ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name','phone','address','avatar')}),
        ('Permissions', {'fields': ('is_seller', 'is_staff', 'is_active','is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_seller', 'is_staff', 'is_active','is_superuser'),
        }),
    )