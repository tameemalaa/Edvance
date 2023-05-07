from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from courses.models import Course, Section

class EnrollWithJoinCodeTestCase(APITestCase):
    def setUp(self):
        self.student = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='password',
            first_name='John',
            last_name='Doe',
            role="2",
        )
        self.course = Course.objects.create(
            name='Test Course',
            description='This is a test course',
            status='1',
            owner=self.student
        )
        self.section = Section.objects.create(
            name='Test Section',
            description='This is a test section',
            course=self.course,
        )


    def test_valid_join_code(self):
        self.client.force_authenticate(self.student)
        response = self.client.post(reverse('courses:enroll_with_join_code', args=[self.section.join_code]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.student in self.section.students.all())

    def test_invalid_join_code(self):
        self.client.force_authenticate(self.student)
        invalid_url = reverse('courses:enroll_with_join_code', args=['invalid_code'])
        response = self.client.post(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(self.student in self.section.students.all())
