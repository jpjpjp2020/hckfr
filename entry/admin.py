from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'role', 'is_superuser_status', 'get_oversight_value', 'get_linked_employers')

    def is_superuser_status(self, obj):
        return obj.is_superuser
    is_superuser_status.short_description = 'Is superuser'
    is_superuser_status.boolean = True

    def get_oversight_value(self, obj):
        if obj.role == 'employer':
            return obj.oversight_value
        return None
    get_oversight_value.short_description = 'Oversight Email'

    def get_linked_employers(self, obj):
        if obj.role == 'oversight':
            return ', '.join([employer.email for employer in obj.oversight_users.all()])
        return None
    get_linked_employers.short_description = 'Linked Employers'
