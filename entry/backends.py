from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            email = User.objects.normalize_email(username)  # Need to use User manager to normalize email
            print("Normalized email:", email)
            user = User.objects.get(email=email)  # Use normalized email
            print("User found:", user.email)

            if user.check_password(password):
                print("Password correct")
                return user
            else:
                print("Password check failed")
                print("Password incorrect")
        except User.DoesNotExist:
            # pass
            print("User not found")
        return None


# class CustomUserBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         try:
#             # username is actually the email
#             user = User.objects.get(email=username)

#             if user.check_password(password):
#                 return user
#         except User.DoesNotExist:
#             # User not found
#             pass
        
#         return None
