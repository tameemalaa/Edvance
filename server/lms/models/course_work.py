from django.db import models
from .course import Course
from .section import Section


class CourseWork(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    points = models.IntegerField()
    data = models.JSONField()  # TODO: Not Sure what's the best way to handle this.

    class Meta:
        abstract = True
