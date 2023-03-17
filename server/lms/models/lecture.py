from django.db import models
from .course import Course

class Lecture(models.Model):
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField() #TODO :are these needed ? 
    video = models.FileField(upload_to="videos/") #TODO : is this the best way to store videos ?
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.course} - {self.date}"
    


    
