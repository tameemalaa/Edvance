from django.db import models
from .course_work import CourseWork

class Quiz(CourseWork):
    started_at = models.DateTimeField()

    def __str__(self):
        return f"Quiz :{self.title} - {self.course} - {self.date}"





