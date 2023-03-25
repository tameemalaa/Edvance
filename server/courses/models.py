from django.db import models
from users.models import User


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

class Section(models.Model):
    name = models.CharField(max_length=255)
    description = (
        models.TextField()
    )  # TODO : why is there a description field in section ?
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    STATUS_CHOICES = [(0, "Past"), (1, "Present"), (2, "Future")]
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES
    )  # TODO : why is there a status field in section shouldn't it just be in the course?
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
