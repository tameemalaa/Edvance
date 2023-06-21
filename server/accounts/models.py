from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

def check_username(username):
    if not username:
        raise ValueError("User must have an username")
    if '@' in username:
        raise ValueError("Username can't include '@'")

def check_email(email):
    if not email:
        raise ValueError("User must have an email")
    
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        check_email(email)
        check_username(username) #TODO : remove this when serializer is working correctly
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        user = self.create_user(email, username, password=password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=255 , null = True)
    gender = models.CharField(max_length=1, choices=[("M", "Male"), ("F", "Female")] , null = True)
    birth_date = models.DateField(null = True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.CharField(
        max_length=1,
        choices=[
            ("1", "Student"),
            ("2", "Teaching Assistant"),
            ("3", "Teacher"),
        ],
        default="1",)
    
    @property
    def role_name(self):
        role_dict = dict(self.ROLE_CHOICES)
        return role_dict.get(self.role)
    
    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name", "last_name" , "role"]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name} - {self.email}"



