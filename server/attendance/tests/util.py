from django.contrib.auth import get_user_model
from courses.models import Course, Section
from lectures.models import Lecture
from attendance.models import Attendance
import random
import string
from datetime import datetime

User = get_user_model()


def generate_test_teacher():
    random_str = "".join(random.choices(string.ascii_lowercase, k=5))
    teacher: User = User.objects.create_user(
        username=f"teacher{random_str}",
        email=f"teacher{random_str}@example.com",
        password="password",
        first_name="John",
        last_name="Doe",
        role="3",
    )
    return teacher


def generate_test_TA():
    random_str = "".join(random.choices(string.ascii_lowercase, k=5))

    TA: User = User.objects.create_user(
        username=f"ta{random_str}",
        email=f"ta{random_str}@example.com",
        password="password",
        first_name="Jane",
        last_name="Doe",
        role="2",
    )
    return TA


def generate_test_student():
    random_str = "".join(random.choices(string.ascii_lowercase, k=5))
    student: User = User.objects.create_user(
        username=f"student{random_str}",
        email=f"student{random_str}@example.com",
        password="password",
        first_name="Bob",
        last_name="Smith",
        role="1",
    )
    return student


def generate_test_course():
    course: Course = Course.objects.create(
        name="Test Course", description="This is a test course"
    )
    return course


def generate_test_section(course: Course):
    section: Section = Section.objects.create(
        name="Test Section",
        description="This is a test section",
        course=course,
        join_code=random.choices(string.ascii_lowercase, k=5),
    )
    return section

def generate_test_lecture(course=None , section= None): 
    if course or section:
        return Lecture.objects.create(  title='Test Lecture', date='2023-01-01',course=course , section=section)
    else: 
        raise ValueError("Either course or section must be provided")
    

def generate_test_attendance_entry(lecture:Lecture , student:User , status:str = "0"):
    return Attendance.objects.create(lecture = lecture , student = student , status = status, date = datetime.now()) 

