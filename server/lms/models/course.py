from django.db import models
from .user import User


class Course(models.Model):
    professor = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    semester = models.CharField(
        max_length=255
    )  # TODO : is semester an attribute for a course ?
    description = models.TextField()
    year = models.IntegerField()
    STATUS_CHOICES = [(0, "Past"), (1, "Present"), (2, "Future")]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.professor_id}"
