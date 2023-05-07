from rest_framework.test import APIClient
from accounts.models import User
from courses.models import Course, Section
from django.urls import reverse
from rest_framework.test import APITestCase

class CourseListViewTestCase(APITestCase):

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

        self.course1 = Course.objects.create(
            name='Course 1',
            description='This is course 1',
            status='1',
            owner= self.teacher
        )
        self.course2 = Course.objects.create(
            name='Course 2',
            description='This is course 2',
            status='2',
            owner = self.teacher2
        )

        self.course1.add_teacher(self.teacher)
        self.course1.add_teacher(self.teacher2)
        self.course2.add_teacher(self.teacher2)

        self.section1 = Section.objects.create(
            name='Section 1',
            description='This is section 1',
            course=self.course1,
            status='1',
        )
        self.section2 = Section.objects.create(
            name='Section 2',
            description='This is section 2',
            course=self.course2,
            status='2',
        )

        self.section1.add_TA(self.ta)

        self.section1.add_student(self.student)

    def test_unauthenticated(self):
        response = self.client.get(reverse('courses:course_list'))
        self.assertEqual(response.status_code, 401)

    def test_teacher(self):  
        self.client.force_authenticate(user=self.teacher)
        response = self.client.get(reverse('courses:course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Course 1')

    def test_TA(self):
        self.client.force_authenticate(user=self.ta)
        response = self.client.get(reverse('courses:course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Course 1')

    def test_student(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get(reverse('courses:course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Course 1')