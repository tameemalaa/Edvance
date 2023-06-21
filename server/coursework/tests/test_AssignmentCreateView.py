from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from accounts.models import User
from courses.models import Course, Section

class AssignmentCreateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='teacher1', email='teacher1@example.com', role='3')
        self.user2 = User.objects.create_user(username='teacher2', email='teacher2@example.com', role='3')
        self.user3 = User.objects.create_user(username='ta1', email='ta1@example.com', role='2')
        self.user4 = User.objects.create_user(username='student1', email='student1@example.com', role='1')
        self.course = Course.objects.create(name='Course 1', owner=self.user1)
        self.section = Section.objects.create(course=self.course)
        self.section.course.teachers.add(self.user2)
        self.section.TAs.add(self.user3)

    def test_teacher_can_create_assignment(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('coursework:assignment_create', args=[self.section.pk])
        data = {
            'title': 'Assignment 1',
            'description': 'Assignment 1 description',
            'due_date': '2023-06-30 23:59:59',
            'max_score': 100
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_other_teacher_can_create_assignment(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('coursework:assignment_create', args=[self.section.pk])
        data = {
            'title': 'Assignment 1',
            'description': 'Assignment 1 description',
            'due_date': '2023-06-30 23:59:59',
            'max_score': 100
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_ta_can_create_assignment(self):
        self.client.force_authenticate(user=self.user3)
        url = reverse('coursework:assignment_create', args=[self.section.pk])
        data = {
            'title': 'Assignment 1',
            'description': 'Assignment 1 description',
            'due_date': '2023-06-30 23:59:59',
            'max_score': 100
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_student_cannot_create_assignment(self):
        self.client.force_authenticate(user=self.user4)
        url = reverse('coursework:assignment_create', args=[self.section.pk])
        data = {
            'title': 'Assignment 1',
            'description': 'Assignment 1 description',
            'due_date': '2023-06-30 23:59:59',
            'max_score': 100
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_user_cannot_create_assignment(self):
        unauthorized_user = User.objects.create_user(username='user1', email='user1@example.com', role='1')
        self.client.force_authenticate(user=unauthorized_user)
        url = reverse('coursework:assignment_create', args=[self.section.pk])
        data = {
            'title': 'Assignment 1',
            'description': 'Assignment 1 description',
            'due_date': '2023-06-30 23:59:59',
            'max_score': 100
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
