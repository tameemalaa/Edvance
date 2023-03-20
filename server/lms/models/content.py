from django.db import models

class Content(models.Model):
    course = models.ForeignKey("Course", on_delete=models.CASCADE , null = True)
    section = models.ForeignKey("Section", on_delete=models.CASCADE , null = True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.CharField(max_length=255) #TODO : no idea what this is

    def __str__(self) -> str:
        return f"{self.title} - {self.course } - {self.section}"