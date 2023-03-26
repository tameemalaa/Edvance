from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=[("M", "Male"), ("F", "Female")])
    birth_date = models.DateField()
    role = models.CharField(
        max_length=1,
        choices=[
            (0, "Super Admin"),
            (1, "Admin"),
            (2, "Teacher"),
            (3, "Teaching Assistant"),
            (4, "Student"),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name} - {self.email}"

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
