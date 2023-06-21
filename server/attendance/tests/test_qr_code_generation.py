from datetime import timedelta
from io import BytesIO
from unittest.mock import patch

from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image
import jwt

from accounts.models import User
from courses.models import Course, Section
from lectures.models import Lecture
from ..models import Attendance
from ..views import GenerateQRAttendance
from .util import generate_test_course, generate_test_student, generate_test_teacher , generate_test_TA , generate_test_section

from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime , timezone , timedelta



class GenerateQRAttendanceTestCase(TestCase):
    def setUp(self):
        course = generate_test_course()
        section = Section.objects.create(name='Test Section', course=course , description = "This is a test section") 
        self.teacher = generate_test_teacher()
        self.student = generate_test_student()
        
        section.students.add(self.student)
        section.save()
        course.teachers.add(self.teacher)
        course.save()
        section.TAs.add(self.teacher)
        section.save()
        self.lecture = Lecture.objects.create(
            title='Test Lecture', date='2023-01-01', course=course, section=section
        )
        self.client = APIClient()
        


    @patch('attendance.views.qrcode.QRCode.make_image')
    def test_generate_qr_code(self, mock_make_image):
        self.client.force_authenticate(user=self.teacher)
        mock_make_image.return_value = Image.new('RGB', (100, 100), color='white')
        url = reverse('generate-qr-attendance', kwargs={'lecture_id': self.lecture.id})
        payload = {'lecture_id': self.lecture.id, 'exp': datetime.now(tz=timezone.utc) + timedelta(seconds=30) }
        token = jwt.encode(payload, 'test_secret_key')
        response = self.client.get(url, {'expire_time_in_minutes': 5})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/png')
        img = Image.open(BytesIO(response.content))
        self.assertEqual(img.size, (100, 100))

    def test_generate_qr_code_with_non_teacher(self):
        self.client.force_authenticate(user=self.student)
        url = reverse('generate-qr-attendance', kwargs={'lecture_id': self.lecture.id})
        payload = {'lecture_id': self.lecture.id, 'exp': datetime.now(tz=timezone.utc) +timedelta(seconds=30) }
        token = jwt.encode(payload, 'test_secret_key')

        response = self.client.get(url, {'expire_time_in_minutes': 5}, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch('attendance.views.qrcode.QRCode.make_image')
    def test_generate_qr_code_for_course_lecture(self, mock_make_image):
        self.client.force_authenticate(user=self.teacher)
        mock_make_image.return_value = Image.new('RGB', (100, 100), color='white')

        course = generate_test_course()
        section = generate_test_section(course)
        for student in range(5):
            student = generate_test_student()
            section.students.add(student)
        section.save()
        course.teachers.add(self.teacher)
        course.save()
        
        lecture = Lecture.objects.create(
            title='Test Lecture', date='2023-01-01',course=course
        )
        payload = {'lecture_id': self.lecture.id, 'exp': datetime.now(tz=timezone.utc) +timedelta(seconds=30) }
        token = jwt.encode(payload, 'test_secret_key')
        url = reverse('generate-qr-attendance', kwargs={'lecture_id': lecture.id})
        response = self.client.get(url, {'expire_time_in_minutes': 5})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/png')
        img = Image.open(BytesIO(response.content))
        self.assertEqual(img.size, (100, 100))
