from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from accounts.models import User
from courses.models import Course, Section
from courses.serializers import SectionSerializer


class SectionCreateViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.teacher = User.objects.create_user(
            username='teacher',
            email='teacher@example.com',
            password='password',
            first_name='John',
            last_name='Doe',
            role="3",
        )
        self.ta = User.objects.create_user(
            username='ta',
            email='ta@example.com',
            password='password',
            first_name='Jane',
            last_name='Doe',
            role="2",
        )
        self.student = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='password',
            first_name='Bob',
            last_name='Smith',
            role="1",
        )
        self.course = Course.objects.create(
            name='Test Course',
            description='This is a test course',
            status='1',
            owner=self.teacher,
        )
    def test_unauthenticated(self):
        url = reverse('courses:section_create', kwargs={'course_pk': self.course.pk})
        data = {
            'name': 'Test Section',
            'description': 'This is a test section',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_student(self):
        self.client.force_authenticate(user=self.student)
        url = reverse('courses:section_create', kwargs={'course_pk': self.course.pk})
        data = {
            'name': 'Test Section',
            'description': 'This is a test section',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_TA(self):
        self.client.force_authenticate(user=self.ta)
        url = reverse('courses:section_create', kwargs={'course_pk': self.course.pk})
        data = {
            'name': 'Test Section',
            'description': 'This is a test section',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        url = reverse('courses:section_create', kwargs={'course_pk': self.course.pk})
        data = {
            'name': 'Test Section',
            'description': 'This is a test section',
            'status': "1",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Section.objects.count(), 1)
        self.assertEqual(Section.objects.get().name, 'Test Section')
        self.assertEqual(Section.objects.get().description, 'This is a test section')
        self.assertEqual(Section.objects.get().course, self.course)

    def test_teacher_bad(self):
        self.client.force_authenticate(user=self.teacher)
        url = reverse('courses:section_create', kwargs={'course_pk': self.course.pk})
        data = {
            'name': 'Test Section',
            'description': 'This is a test section',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_teacher_with_TA(self):
        self.client.force_authenticate(user=self.teacher)
        url = reverse('courses:section_create', kwargs={'course_pk': self.course.pk})
        data = {
            'name': 'Test Section',
            'description': 'This is a test section',
            'status': "1",
            'TA_email': self.ta.email,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Section.objects.count(), 1)
        self.assertEqual(Section.objects.get().name, 'Test Section')
        self.assertEqual(Section.objects.get().description, 'This is a test section')
        self.assertEqual(Section.objects.get().course, self.course)
        self.assertIn(self.ta, Section.objects.get().TAs.all())
