from django.db import models
from accounts.models import User
from courses.models import Course, Section


# class CourseWork(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     section = models.ForeignKey(Section, on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     due_date = models.DateField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     points = models.IntegerField()
#     data = models.JSONField()  # TODO: Not Sure what's the best way to handle this.

#     class Meta:
#         abstract = True


# class Assignment(CourseWork):
#     def __str__(self) -> str:
#         return f"Assignment :{self.title} - {self.course} - {self.date}"


# # class Quiz(CourseWork):
# #     started_at = models.DateTimeField()

# #     def __str__(self):
# #         return f"Quiz :{self.title} - {self.course} - {self.date}"


# class Submission(models.Model):
#     student = models.ForeignKey(User, on_delete=models.CASCADE)
#     date = models.DateField()
#     data = models.JSONField()
#     score = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         abstract = True


# class assignmentSubmission(Submission):
#     assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)


# class quizSubmission(Submission):
#     quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)


# class Question(models.Model):
#     quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
#     text = models.TextField()
#     data = models.JSONField()  # TODO: Not Sure what's the best way to handle this.
#     points = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.text} - {self.quiz}"


from django.db import models
from accounts.models import User
from courses.models import Course


class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_assignments')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='section_assignments')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_assignments', default=None)
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    max_score = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.title


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='assignment_submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_submissions')
    file = models.FileField(upload_to='submissions/')
    text_submission = models.TextField(blank=True,null=True)
    link_submission = models.URLField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.assignment.title} - {self.student.username}"


class Review(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    feedback = models.TextField()
    score = models.PositiveIntegerField()

    def __str__(self):
        return f"Review for {self.submission.assignment.title} by {self.reviewer.username}"


class Grade(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='grade')
    grader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='graded_submissions')
    score = models.PositiveIntegerField()
    comments = models.TextField(blank=True)

    def __str__(self):
        return f"Grade for {self.submission.assignment.title} - {self.submission.student.username}"


# class Announcement(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='announcements')
#     title = models.CharField(max_length=200)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title
