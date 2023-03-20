from django.db import models

class Submission(models.Model):
    student = models.ForeignKey("user", on_delete=models.CASCADE)
    date = models.DateField()
    data = models.JSONField()
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class assignmentSubmission(Submission):
    assignment = models.ForeignKey("Assignment", on_delete=models.CASCADE)

class quizSubmission(Submission):
    quiz = models.ForeignKey("Quiz", on_delete=models.CASCADE)