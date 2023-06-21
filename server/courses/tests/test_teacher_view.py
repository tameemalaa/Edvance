from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from accounts.models import User
from courses.models import Course, Section

class TeacherViewTestCase(APITestCase):
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
        self.teacher2 = User.objects.create_user(
            username='teacher2',
            email='teacher2@example.com',
            password='password',
            first_name='John2',
            last_name='Doe2',
            role="3",
        )
        self.course = Course.objects.create(
            name='Test Course',
            description='This is a test course',
            status='1',
            owner=self.teacher
        )
        self.course.add_teacher(self.teacher)
        self.course.add_teacher(self.teacher2)

        self.url = reverse('courses:teacher', args=[self.course.pk])
    
    def test_teacher_add_teacher(self):
        self.client.force_authenticate(self.teacher)
        new_teacher = User.objects.create_user(
            username='new_teacher',
            email='new_teacher@example.com',
            password='password',
            first_name='Jane',
            last_name='Doe',
            role="3",
        )
        data = {
            'teacher_email': new_teacher.email
        }
        response = self.client.post(self.url, {'teacher_email': new_teacher.email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(new_teacher in self.course.teachers.all())
    
    def test_teacher_remove_teacher(self):
        self.client.force_authenticate(self.teacher)
        new_teacher = User.objects.create_user(
            username='new_teacher',
            email='new_teacher@example.com',
            password='password',
            first_name='Jane',
            last_name='Doe',
            role="3",
        )
        self.course.add_teacher(new_teacher)
        data = {
            'teacher_id': new_teacher.id
        }
        response = self.client.delete(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(new_teacher in self.course.teachers.all())
    
    def test_teacher_remove_owner(self):
        self.client.force_authenticate(self.teacher2)

        data = {
            'teacher_id': self.teacher.id
        }
        response = self.client.delete(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(self.teacher in self.course.teachers.all())