from django.db import models 
from .quiz import Quiz

class Question(models.Model): 
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()
    data = models.JSONField() # TODO: Not Sure what's the best way to handle this.
    points = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.text} - {self.quiz}"
