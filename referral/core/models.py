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

    def create_superuser(self, email, password, **other_fields):
        user = self.create_user(
            email = self.normalize_email(email),
            password=password,
            **other_fields
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
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
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    link = models.URLField(max_length=70)
    clicks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    closing_date = models.DateField()
    is_active = models.BooleanField(default=True)
    #adding campaign description
    description = models.TextField()


class Candidate(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    referral_code = models.CharField(max_length=10)
    clicks = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        code = secrets.token_urlsafe(6)
        exist = Candidate.objects.filter(referral_code=code).exists()
        while exist:
            code = secrets.token_urlsafe(6)
        self.referral_code = code
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - {self.referral_code}'

    class Meta:
        ordering = ['clicks']


class CampaignClick(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    mac_ad = models.CharField(max_length=14)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.campaign.name} - {self.mac_ad}'


