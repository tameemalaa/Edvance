from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from accounts.models import User
from courses.models import Course, Section
from coursework.models import Assignment, Submission
from django.core.files.uploadedfile import SimpleUploadedFile


class AssignmentSubmissionViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.student = User.objects.create_user(username='student1', email='student1@example.com', role='1')
        self.teacher = User.objects.create_user(username='teacher1', email='teacher1@example.com', role='3')
        self.course = Course.objects.create(name='Course 1', owner=self.teacher)
        self.section = Section.objects.create(course=self.course)
        self.section.students.add(self.student)
        self.assignment = Assignment.objects.create(course=self.course, section=self.section,
                                                    creator=self.teacher, title='Assignment 1',
                                                    description='Assignment 1 description',
                                                    due_date='2023-06-30 23:59:59', max_score=100)

    def test_successful_submission_with_file(self):
        self.client.force_authenticate(user=self.student)
        url = reverse('coursework:assignment_submit', args=[self.assignment.pk])
        # Prepare a sample file for submission
        file_content = b'This is a sample file content'
        submitted_file = SimpleUploadedFile('sample_file.txt', file_content)
        data = {
            'file': submitted_file
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Assignment submitted successfully.')
        # Additional assertions to check the created submission object
        submission = Submission.objects.get(assignment=self.assignment, student=self.student)
        self.assertEqual(submission.file.read(), file_content)
        # Clean up the uploaded file
        submission.file.delete()

    def test_successful_submission_with_text_submission(self):
        self.client.force_authenticate(user=self.student)
        url = reverse('coursework:assignment_submit', args=[self.assignment.pk])
        text_submission = 'This is a text submission.'
        data = {
            'text_submission': text_submission
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Assignment submitted successfully.')
        # Additional assertions to check the created submission object
        submission = Submission.objects.get(assignment=self.assignment, student=self.student)
        self.assertEqual(submission.text_submission, text_submission)

    def test_successful_submission_with_link_submission(self):
        self.client.force_authenticate(user=self.student)
        url = reverse('coursework:assignment_submit', args=[self.assignment.pk])
        link_submission = 'https://example.com'
        data = {
            'link_submission': link_submission
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Assignment submitted successfully.')
        # Additional assertions to check the created submission object
        submission = Submission.objects.get(assignment=self.assignment, student=self.student)
        self.assertEqual(submission.link_submission, link_submission)

    def test_submission_unauthorized(self):
        self.client.force_authenticate(user=self.teacher)
        url = reverse('coursework:assignment_submit', args=[self.assignment.pk])
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        unauthorized_user = User.objects.create_user(username='unauthorized', email='unauthorized@example.com', role='1')
        self.client.force_authenticate(user=unauthorized_user)
        url = reverse('coursework:assignment_submit', args=[self.assignment.pk])
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_submission_invalid_assignment(self):
        self.client.force_authenticate(user=self.student)
        url = reverse('coursework:assignment_submit', args=[9999])  # Nonexistent assignment pk
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_user_submission(self):
        unauthorized_user = User.objects.create_user(username='unauthorized', email='unauthorized@example.com', role='1')
        self.client.force_authenticate(user=unauthorized_user)
        url = reverse('coursework:assignment_submit', args=[self.assignment.pk])
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_submission_without_required_data(self):
        self.client.force_authenticate(user=self.student)
        url = reverse('coursework:assignment_submit', args=[self.assignment.pk])
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'At least one submission field is required.')