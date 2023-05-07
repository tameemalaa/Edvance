from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from accounts.models import User
from courses.models import Course
from courses.serializers import CourseSerializer


class CourseCreateViewTestCase(APITestCase):
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
    def test_unauthenticated(self):
        url = reverse('courses:course_create')
        data = {
            'name': 'Test Course',
            'description': 'This is a test course',
            'status': '1',
        }
        response = self.client.post(url, data, format='json')
        response = self.client.get(reverse('courses:course_list'))
        self.assertEqual(response.status_code, 401)

    def test_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        url = reverse('courses:course_create')
        data = {
            'name': 'Test Course',
            'description': 'This is a test course',
            'status': '1',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(Course.objects.get().name, 'Test Course')
        self.assertEqual(Course.objects.get().description, 'This is a test course')
        self.assertEqual(Course.objects.get().status, '1')
        self.assertEqual(Course.objects.get().owner, self.teacher)

    def test_teacher_bad_data(self):
        self.client.force_authenticate(user=self.teacher)
        url = reverse('courses:course_create')
        data = {
            'name': 'Test Course',
            'description': 'This is a test course',
            'status': '5',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_TA(self):
        self.client.force_authenticate(user=self.ta)
        url = reverse('courses:course_create')
        data = {
            'name': 'Test Course',
            'description': 'This is a test course',
            'status': '1',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student(self):
        self.client.force_authenticate(user=self.student)
        url = reverse('courses:course_create')
        data = {
            'name': 'Test Course',
            'description': 'This is a test course',
            'status': '1',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
