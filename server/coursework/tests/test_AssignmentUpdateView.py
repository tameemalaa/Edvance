from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from accounts.models import User
from courses.models import Course, Section
from coursework.models import  Assignment
from coursework.serializers import AssignmentSerializer
from django.utils import timezone
import datetime
import time

def datetime_from_utc_to_local(utc_datetime):
        now_timestamp = time.time()
        offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
        return utc_datetime + offset

class AssignmentUpdateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='teacher1', email='teacher1@example.com', role='3')
        self.user2 = User.objects.create_user(username='teacher2', email='teacher2@example.com', role='3')
        self.user3 = User.objects.create_user(username='ta1', email='ta1@example.com', role='2')
        self.course = Course.objects.create(name='Course 1', owner=self.user1)
        self.section = Section.objects.create(course=self.course)
        self.section.course.teachers.add(self.user2)
        self.section.TAs.add(self.user3)
        self.assignment = Assignment.objects.create(course=self.course, section=self.section,
                                                    creator=self.user1, title='Assignment 1',
                                                    description='Assignment 1 description',
                                                    due_date='2023-06-30 23:59:59', max_score=100)

    


    def test_get_assignment(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('coursework:assignment_update', args=[self.assignment.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.assignment.id)
        self.assertEqual(response.data['title'], self.assignment.title)
        self.assertEqual(response.data['description'], self.assignment.description)

        expected_due_date = datetime.datetime.strptime('2023-06-30 23:59:59', '%Y-%m-%d %H:%M:%S')
        actual_due_date = datetime.datetime.strptime(response.data['due_date'], '%Y-%m-%dT%H:%M:%SZ')
        self.assertEqual(actual_due_date, expected_due_date)
        self.assertEqual(response.data['max_score'], self.assignment.max_score)

    def test_update_assignment(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('coursework:assignment_update', args=[self.assignment.pk])
        data = {
            'title': 'Updated Assignment 1',
            'description': 'Updated Assignment 1 description',
            'due_date': '2023-07-31 23:59:59',
            'max_score': 200
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assignment.refresh_from_db()
        self.assertEqual(self.assignment.title, 'Updated Assignment 1')
        self.assertEqual(self.assignment.description, 'Updated Assignment 1 description')
        expected_due_date = timezone.make_aware(datetime.datetime(2023, 7, 31, 23, 59, 59))
        self.assertEqual(self.assignment.due_date, expected_due_date)
        self.assertEqual(self.assignment.max_score, 200)

    def test_unauthorized_user_cannot_update_assignment(self):
        unauthorized_user = User.objects.create_user(username='user1', email='user1@example.com', role='1')
        self.client.force_authenticate(user=unauthorized_user)
        url = reverse('coursework:assignment_update', args=[self.assignment.pk])
        data = {
            'title': 'Updated Assignment',
            'description': 'Updated Assignment description',
            'due_date': '2023-07-31 23:59:59',
            'max_score': 90
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_assignment(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('coursework:assignment_update', args=[self.assignment.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Assignment.objects.filter(pk=self.assignment.pk).exists())

    def test_unauthorized_user_cannot_delete_assignment(self):
        unauthorized_user = User.objects.create_user(username='user1', email='user1@example.com', role='1')
        self.client.force_authenticate(user=unauthorized_user)
        url = reverse('coursework:assignment_update', args=[self.assignment.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Assignment.objects.filter(pk=self.assignment.pk).exists())

    def test_get_assignment_unauthorized(self):
        unauthorized_user = User.objects.create_user(username='user1', email='user1@example.com', role='1')
        self.client.force_authenticate(user=unauthorized_user)
        url = reverse('coursework:assignment_update', args=[self.assignment.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_nonexistent_assignment(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('coursework:assignment_update', args=[9999])  # Nonexistent assignment pk
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_nonexistent_assignment(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('coursework:assignment_update', args=[9999])  # Nonexistent assignment pk
        data = {
            'title': 'Updated Assignment',
            'description': 'Updated Assignment description',
            'due_date': '2023-07-31 23:59:59',
            'max_score': 200
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_assignment(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('coursework:assignment_update', args=[9999])  # Nonexistent assignment pk
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)