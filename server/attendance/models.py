from django.db import models
from accounts.models import User
from lectures.models import Lecture

ABSENCE_STATUS_CHOICES = [("0", "Absent"), ("1", "Present"), ("2", "Late"), ("3", "Excused")]

class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    status = models.CharField(max_length=1, choices=ABSENCE_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'lecture'], name='One lecture record per student')
        ]
    

    def __str__(self):
        return f"{self.student_id} - {self.lecture_id} - {self.status}"
