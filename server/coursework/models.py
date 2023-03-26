from django.db import models
from accounts.models import User
from courses.models import Course, Section


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


class Assignment(CourseWork):
    def __str__(self) -> str:
        return f"Assignment :{self.title} - {self.course} - {self.date}"


class Quiz(CourseWork):
    started_at = models.DateTimeField()

    def __str__(self):
        return f"Quiz :{self.title} - {self.course} - {self.date}"


class Submission(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    data = models.JSONField()
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class assignmentSubmission(Submission):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)


class quizSubmission(Submission):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()
    data = models.JSONField()  # TODO: Not Sure what's the best way to handle this.
    points = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.text} - {self.quiz}"
