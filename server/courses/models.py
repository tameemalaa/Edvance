from django.db import models
from accounts.models import User


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    year = models.IntegerField()
    STATUS_CHOICES = [("0", "Past"), ("1", "Present"), ("2", "Future")]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    teachers = models.ManyToManyField(User, related_name="courses")

    def __str__(self):
        return f"{self.name} - {self.year} - {self.status}"


class Section(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    STATUS_CHOICES = [("0", "Past"), ("1", "Present"), ("2", "Future")]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    assistants = models.ManyToManyField(User, related_name="sections")

    def __str__(self):
        return f"{self.name} - {self.course} - {self.status}"
