from django.db import models
from accounts.models import User
import string
import random
from django.core.mail import send_mail


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    STATUS_CHOICES = [("0", "Past"), ("1", "Present"), ("2", "Future")]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # owner = models.ForeignKey(User, on_delete=models.CASCADE)
    teachers = models.ManyToManyField(User, related_name="courses")

    def __str__(self):
        return f"{self.name} - {self.status}"
    
    def add_teacher(self, user):
        self.teachers.add(user)
        self.send_invitation_email(user)

    def send_invitation_email(self, user):
        subject = f"You have been added as a teacher to {self.name}"
        message = f"Dear {user.first_name},\n\nYou have been added as a teacher to {self.name}. " \
                  f"Please log in to your account to accept the invitation.\n\nBest regards,\n" \
                  f"The Course Management Team"
        from_email = "coursemanagement@example.com"
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)

    


class Section(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    STATUS_CHOICES = [("0", "Past"), ("1", "Present"), ("2", "Future")]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    TAs = models.ManyToManyField(User, related_name="managed_sections") # TODO : change these names 
    students = models.ManyToManyField(User, related_name="section_enrollment")
    join_code = models.CharField(max_length=10, unique=True)

    def generate_join_code(self):
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
        code = ''.join(random.choice(chars) for _ in range(10))
        self.join_code = code
        self.save()

    def __str__(self):
        return f"{self.name} - {self.course} - {self.status} - {self.join_code}"
    

    def add_TA(self, user):
        self.TAs.add(user)
        self.send_invitation_email(user)

    def add_student(self, user):
        self.students.add(user)
        self.send_invitation_email(user)

    def join_student(self, user, join_code):
        if self.filter(join_code=join_code).exists():
            section = self.get(join_code=join_code)
            section.students.add(user)
            section.send_invitation_email(user)
        else:
            raise Exception("Invalid join code")


    def send_invitation_email(self, user):
        subject = f"You have been added as a {user.role_name} to {self.course.name} - {self.name}"
        message = f"Dear {user.first_name},\n\nYou have been added as a TA or student to {self.course.name} - " \
                  f"{self.name}. Please log in to your account to accept the invitation.\n\nBest regards,\n" \
                  f"The Course Management Team"
        from_email = "coursemanagement@example.com"
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)

    
    def remove_student(self, user):
        self.students.remove(user)

    def remove_TA(self, user):
        self.TAs.remove(user)