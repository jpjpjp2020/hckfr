from django.shortcuts import redirect
from django.urls import reverse


class RestrictAdminMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(reverse('admin:index')):
            if not request.user.is_superuser:
                return redirect('/')
        return self.get_response(request)
    

# Pos better UX modification and aded imports - sending to db not /
# from django.contrib.auth import get_user_model

# User = get_user_model()


# class RestrictAdminMiddleware:

#     def __init__(self, get_response):
#         self.get_response = get_response

#     if request.path.startswith(reverse('admin:index')):
#             if request.user.is_authenticated:
#                 if not request.user.is_superuser:
#                     # Redirect based on user role
#                     if request.user.role == 'employer':
#                         return redirect('feedback:employer_dashboard')
#                     # More role-based elif conditions
#                     else:
#                         return redirect('/')
#             else:
#                 # Allow unauthenticated users to reach the admin login page
#                 pass
#         return self.get_response(request)