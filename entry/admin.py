from django.contrib import admin
from django.utils.html import format_html
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'role', 'is_active', 'is_superuser_status', 'get_oversight_value', 'password_hash')  # remove pasword hash later!!!
    search_fields = ('email', 'username', 'role')
    list_filter = ('role', 'is_superuser')

    def is_superuser_status(self, obj):
        return obj.is_superuser
    is_superuser_status.short_description = 'Is superuser'
    is_superuser_status.boolean = True

    def get_oversight_value(self, obj):
        if obj.role == 'employer':
            return obj.oversight_value
        return None
    get_oversight_value.short_description = 'Oversight Value'

    def is_active(self, obj):
        return obj.is_active
    is_active.short_description = 'Is Active'
    is_active.boolean = True

    def password_hash(self, obj):
        return format_html("<code>{}</code>", obj.password)
    password_hash.short_description = 'Password Hash'
