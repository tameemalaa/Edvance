from django.db import models
from .course_work import CourseWork

class Assignment(CourseWork):
    
    def __str__(self) -> str:
        return f"Assignment :{self.title} - {self.course} - {self.date}"


