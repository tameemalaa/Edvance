from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from accounts.models import User
from courses.models import Course, Section
from ..models import Assignment

class AssignmentDetailViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='student1', email='student1@example.com', role='1')
        self.user2 = User.objects.create_user(username='teacher1', email='teacher1@example.com', role='3')
        self.user3 = User.objects.create_user(username='ta1', email='ta1@example.com', role='2')
        self.course = Course.objects.create(name='Course 1', owner=self.user2)
        self.section = Section.objects.create(course=self.course)
        self.section.students.add(self.user1)
        self.section.TAs.add(self.user3)
        self.assignment1 = Assignment.objects.create(
            course=self.course,
            section=self.section,
            creator=self.user2,
            title='Assignment 1',
            description='Assignment 1 description',
            due_date='2023-06-30 23:59:59',
            max_score=100
        )
        self.assignment2 = Assignment.objects.create(
            course=self.course,
            section=self.section,
            creator=self.user2,
            title='Assignment 2',
            description='Assignment 2 description',
            due_date='2023-07-07 23:59:59',
            max_score=100
        )

    def test_student_can_view_assignment_details(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('coursework:assignment_detail', args=[self.assignment1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Assignment 1')

        url = reverse('coursework:assignment_detail', args=[self.assignment2.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Assignment 2')

    def test_teacher_can_view_assignment_details(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('coursework:assignment_detail', args=[self.assignment1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Assignment 1')

        url = reverse('coursework:assignment_detail', args=[self.assignment2.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Assignment 2')

    def test_ta_can_view_assignment_details(self):
        self.client.force_authenticate(user=self.user3)
        url = reverse('coursework:assignment_detail', args=[self.assignment1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Assignment 1')

        url = reverse('coursework:assignment_detail', args=[self.assignment2.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Assignment 2')

    def test_unauthorized_user_cannot_view_assignment_details(self):
        unauthorized_user = User.objects.create_user(username='user1', email='user1@example.com')
        self.client.force_authenticate(user=unauthorized_user)
        url = reverse('coursework:assignment_detail', args=[self.assignment1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse('coursework:assignment_detail', args=[self.assignment2.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
