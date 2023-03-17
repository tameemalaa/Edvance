from django.db import models


class User(models.model):
    role = models.ForeignKey("UserRole", on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255) 
    phone = models.CharField(
        max_length=255
    )  # TODO : a better way is possible with a third party library
    GENDER_CHOICES = [("M", "Male"), ("F", "Female")]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name} - {self.email}"


class UserRole(models.model):
    ROLE_CHOICES = [
        (0, "Super Admin"),
        (1, "Admin"),
        (2, "Teacher"),
        (3, "Teaching Assitant"),
        (4, "Student"),
    ]
    role = models.CharField(max_length=1, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.get_role_display()}"
