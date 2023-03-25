from django.db import models
from users.models import User
from lectures.models import Lecture


class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    STATUS_CHOICES = [(0, "Absent"), (1, "Present"), (2, "Late"), (3, "Excused")]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student_id} - {self.lecture_id} - {self.status}"
