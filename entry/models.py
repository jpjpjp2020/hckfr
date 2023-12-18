from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _


# acc creation into CustomUserManager and base user as class User
# !!! oversight value not oversight email !!!

class CustomUserManager(BaseUserManager):
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if email is None:
            raise ValueError(_('Superusers must have an email.'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_worker_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError(_('Username is required'))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.role = 'worker'
        user.save(using=self._db)
        return user

    def create_employer_user(self, email, password=None, oversight_email=None, **extra_fields):
        if not email:
            raise ValueError(_('Email is required'))
        email = self.normalize_email(email)
        user = self.model(email=email, oversight_email=oversight_email, **extra_fields)
        user.set_password(password)
        user.role = 'employer'
        user.save(using=self._db)
        return user

    def create_oversight_user(self, email, employer, password=None, **extra_fields):
        if not email:
            raise ValueError(_('Email is required'))
        email = self.normalize_email(email)
        user = self.model(email=email, employer=employer, **extra_fields)
        user.set_password(password)
        user.role = 'oversight'
        user.save(using=self._db)
        return user
        
    

# unified auth:
    
class User(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(max_length=25, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    employer = models.ForeignKey('self', on_delete=models.CASCADE, related_name='oversight_users', null=True, blank=True)
    oversight_email = models.EmailField(null=True, blank=True)  # use value but def as email in form rendering
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    ROLE_CHOICES = (
        ('worker', 'Worker'),
        ('employer', 'Employer'),
        ('oversight', 'Oversight'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    USERNAME_FIELD = 'email'  # primary identifier
    REQUIRED_FIELDS = ['username']  # required only for workers

    objects = CustomUserManager()
    
    @property
    def is_oversight(self):
        return self.role == 'oversight' and self.employer is not None

    def __str__(self):
        return self.email or self.username