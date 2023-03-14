from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import secrets


class UserManager(BaseUserManager):
    def create_user(self, email, password, **other_fields):
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **other_fields
        )
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=15, blank=True)
    company_name = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone"]

    objects = UserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Campaign(models.Model):
    name = models.CharField(max_length=50, unique=True)
    link = models.URLField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    closing_date = models.DateField()
    clicks = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)




