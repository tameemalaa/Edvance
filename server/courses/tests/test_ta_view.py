from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from accounts.models import User
from courses.models import Course, Section


class TAViewTestCase(APITestCase):
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
        self.TA = User.objects.create_user(
            username='TA',
            email='TA@example.com',
            password='password',
            first_name='Jane',
            last_name='Doe',
            role="2",
        )
        self.TA2 = User.objects.create_user(
            username='TA2',
            email='TA2@example.com',
            password='password',
            first_name='Jane2',
            last_name='Doe2',
            role="2",
        )
        self.course = Course.objects.create(
            name='Test Course',
            description='This is a test course',
            status='1',
            owner=self.teacher
        )
        self.course.add_teacher(self.teacher)

        self.section = Section.objects.create(
            name='Test Section',
            course=self.course
        )
        self.section.add_TA(self.TA)

        self.url = reverse('courses:ta', args=[self.section.pk])

    def test_add_TA(self):
        self.client.force_authenticate(user=self.teacher)
        User.objects.create_user(
            username='new_ta',
            email='new_ta@example.com',
            password='password',
            first_name='Jane',
            last_name='Doe',
            role="3",
        )
        data = {'TA_email': 'new_ta@example.com'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_ta = User.objects.get(email='new_ta@example.com')
        self.assertTrue(new_ta in self.section.TAs.all())

    def test_add_TA_unauthorized(self):
        self.client.force_authenticate(user=self.TA2)
        User.objects.create_user(
            username='new_ta',
            email='new_ta@example.com',
            password='password',
            first_name='Jane',
            last_name='Doe',
            role="3",
        )
        data = {'TA_email': 'new_ta@example.com'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('new_ta@example.com' in [ta.email for ta in self.section.TAs.all()])

    def test_remove_TA(self):
        self.client.force_authenticate(user=self.teacher)
        data = {'TA_id': self.TA.pk}
        response = self.client.delete(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.TA in self.section.TAs.all())

    def test_remove_TA_unauthorized(self):
        self.client.force_authenticate(user=self.TA2)
        data = {'TA_id': self.TA.pk}
        response = self.client.delete(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(self.TA in self.section.TAs.all())
