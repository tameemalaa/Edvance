from django.db import models
from courses.models import Course, Section


class Material(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.CharField(max_length=255)
    CATEGORY_CHOICES = [("0" , "lecture slides"), ("1" , "reading"), ("2" , "video lecture"), ("3" , "other")]
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES)

    def __str__(self) -> str:
        return f"{self.title} - {self.course } - {self.section}"
