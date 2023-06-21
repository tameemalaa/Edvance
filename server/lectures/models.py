from django.db import models
from courses.models import Course, Section


class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True , blank = True )
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True , blank = True)
    title = models.CharField(max_length=255 , null = True , blank = True)
    description = models.TextField(null = True, blank = True)
    video_link = models.CharField(max_length=255, null = True, blank = True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    


    def __str__(self):
        return f"{self.title} - {self.course} - {self.date}"
