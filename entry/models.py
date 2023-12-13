from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, username=None, password=None, **extra_fields):
        if not email and not username:
            raise ValueError(_('Email or Username is required'))
        if email:
            email = self.normalize_email(email)
            user = self.model(email=email, **extra_fields)
        else:
            user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError(_('Superuser must have is_staff=True.'))
        if not extra_fields.get('is_superuser'):
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, username, password, **extra_fields)


class WorkerUser(AbstractBaseUser):
    username = models.CharField(max_length=25, unique=True)

    USERNAME_FIELD = 'username'
    objects = CustomUserManager()

    def __str__(self):
        return self.username


class ManagementUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    oversight_email = models.EmailField()

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class OversightUser(AbstractBaseUser):
    email = models.ForeignKey(ManagementUser, on_delete=models.CASCADE, related_name='oversight_users')  # consider data retention policy edge cases later on
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)
