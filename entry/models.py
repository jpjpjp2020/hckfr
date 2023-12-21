from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _


# acc creation into CustomUserManager and base user as class User
# !!! oversight value not oversight email !!!

class CustomUserManager(BaseUserManager):
    
    # internal:

    def create_superuser(self, email, password, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.role = 'admin'
        user.save(using=self._db)
        return user
    
    # external:

    def create_employer_user(self, email, password=None, oversight_value=None, **extra_fields):
        if not email:
            raise ValueError(_('Email is required'))
        email = self.normalize_email(email)
        user = self.model(email=email, oversight_value=oversight_value, **extra_fields)
        user.set_password(password)
        user.role = 'employer'
        user.save(using=self._db)
        return user        
    

# unified auth:
    
class User(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(unique=True)
    oversight_value = models.EmailField(null=True, blank=True)  # use value but def as email in form rendering
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    ROLE_CHOICES = (
        ('employer', 'Employer'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    USERNAME_FIELD = 'email'  

    objects = CustomUserManager()

    def __str__(self):
        return self.email