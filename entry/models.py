from django.db import models
from django.core.exceptions import ValidationError
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
    # employer:

    def create_employer_user(self, email, password=None, oversight_value=None, **extra_fields):
        if not email:
            raise ValueError(_('Email is required'))
        email = self.normalize_email(email)
        user = self.model(email=email, oversight_value=oversight_value, **extra_fields)
        user.set_password(password)
        user.role = 'employer'
        user.is_active = True  # explicitly set is_active to True
        user.save(using=self._db)
        return user
    
    # oversight:
    
    def create_oversight_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('Email is required'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.role = 'oversight'
        user.is_active = True
        user.save(using=self._db)
        return user
    
    # employee:

    def create_worker_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError(_('Username is required'))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.role = 'worker'
        user.is_active = True
        user.save(using=self._db)
        return user
    

# unified auth:
    
class User(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(unique=True, null=True, blank=True)
    oversight_value = models.EmailField(null=True, blank=True)  # use value but def as email in form rendering
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(max_length=50, unique=True, null=True, blank=True)
    # plaeholders for feature expansion
    # custom_feedback_window = models.IntegerField(null=True, blank=True)
    # custom_data_retention_period = models.IntegerField(null=True, blank=True)
    # also need one for active feedback window at one point

    ROLE_CHOICES = (
        ('employer', 'Employer'),
        ('oversight','Oversight'),
        ('worker', 'Worker'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def clean(self):

        super().clean()
        if self.role == 'worker':
            if not self.username:
                raise ValidationError("Username is required for worker accounts.")
        else:
            if not self.email:
                raise ValidationError("Email is required for employer and oversight accounts.")
            if self.email == self.oversight_value:
                raise ValidationError("Oversight email cannot be the same as your email.")

    def __str__(self):
        if self.role == 'worker':
            return self.username
        return self.email
