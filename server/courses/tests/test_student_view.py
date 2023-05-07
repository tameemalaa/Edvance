from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from accounts.models import User
from courses.models import Course, Section

class StudentViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)
        self.teacher = User.objects.create_user(
            username='teacher',
            email='teacher@example.com',
            password='password',
            first_name='John',
            last_name='Doe',
            role="3",
        )
        self.student = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='password',
            first_name='Jane',
            last_name='Doe',
            role="2",
        )
        self.course = Course.objects.create(
            name='Test Course',
            description='This is a test course',
            status='1',
            owner=self.teacher
        )
        self.section = Section.objects.create(
            name='Test Section',
            description='This is a test section',
            course=self.course
        )
        self.course.add_teacher(self.teacher)
        self.section.add_student(self.student)

        self.url = reverse('courses:student', args=[self.section.pk])
    
    def test_student_add(self):
        self.client.force_authenticate(self.teacher)
        new_student = User.objects.create_user(
            username='new_student',
            email='new_student@example.com',
            password='password',
            first_name='Jake',
            last_name='Doe',
            role="2",
        )
        data = {
            'student_email': new_student.email
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(new_student in self.section.students.all())
    
    def test_student_remove(self):
        self.client.force_authenticate(self.teacher)
        data = {
            'student_id': self.student.id
        }
        response = self.client.delete(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.student in self.section.students.all())
    
    def test_student_add_unauthenticated(self):
        new_student = User.objects.create_user(
            username='new_student',
            email='new_student@example.com',
            password='password',
            first_name='Jake',
            last_name='Doe',
            role="2",
        )
        data = {
            'student_email': new_student.email
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(new_student in self.section.students.all())
    
    def test_student_remove_unauthenticated(self):
        data = {
            'student_id': self.student.id
        }
        response = self.client.delete(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(self.student in self.section.students.all())

    def test_student_remove_unauthorized(self):
        self.client.force_authenticate(self.student)
        data = {
            'student_id': self.student.id
        }
        response = self.client.delete(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(self.student in self.section.students.all())
    
    def test_student_add_unauthorized(self):
        self.client.force_authenticate(self.student)
        new_student = User.objects.create_user(
            username='new_student',
            email='new_student@example.com',
            password='password',
            first_name='Jake',
            last_name='Doe',
            role="2",
        )
        data = {
            'student_email': new_student.email
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(new_student in self.section.students.all())
