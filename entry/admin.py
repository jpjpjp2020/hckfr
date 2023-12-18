from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'oversight_email', 'get_employer_email', 'username', 'role', 'is_superuser_status')
    
    def is_superuser_status(self, obj):
        return obj.is_superuser
    is_superuser_status.short_description = 'Is superuser'
    is_superuser_status.boolean = True

    def get_employer_email(self, obj):
        if obj.role == 'oversight' and obj.employer:
            return obj.employer.email
        return None
    get_employer_email.short_description = 'Employer Email'
