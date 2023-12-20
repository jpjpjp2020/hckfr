from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q

User = get_user_model()

class CustomUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print("Custom authentication backend called")
        print("Username/Email:", username)
        print("Role:", kwargs.get('role', 'None'))

        try:
            if User.objects.filter(email=username, is_superuser=True).exists():
                print("Attempting to authenticate superuser")
                user = User.objects.get(email=username, is_superuser=True)
            # username for w
            elif 'role' in kwargs and kwargs['role'] == 'worker':
                print("Attempting to authenticate worker")
                user = User.objects.get(username=username, role='worker')
            else:
                # email for e and o
                print("Attempting to authenticate employer or oversight")
                user = User.objects.get(email=username, role__in=['employer', 'oversight'])
            
            if user.check_password(password):
                print("Password correct, authentication successful")
                return user
            else:
                print("Password incorrect, authentication failed")
        except User.DoesNotExist:
            print("User does not exist")
            User().set_password(password)
        except MultipleObjectsReturned:
            print("Multiple users returned, authentication failed")
            return None

