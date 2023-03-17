from django.db import models
from .user import User
from .course import Course


class Section(models.Model):
    name = models.CharField(max_length=255)
    discritpion = (
        models.TextField()
    )  # TODO : why is there a discription field in section ?
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, null = True , on_delete=models.SET_NULL)
    STATUS_CHOICES = [(0, "Past"), (1, "Present"), (2, "Future")]
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES
    )  # TODO : why is there a status field in section ?
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    students = models.ManyToManyField("User", related_name="sections")

    def __str__(self):
        return f"{self.name} - {self.course_id}"


