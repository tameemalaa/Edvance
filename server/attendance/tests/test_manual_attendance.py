from django.test import TestCase
from rest_framework.test import APIClient
from attendance.serializers import AttendanceSerializer
from .util import (
    generate_test_course,
    generate_test_student,
    generate_test_teacher,
    generate_test_TA,
    generate_test_section,
    generate_test_lecture,
    generate_test_attendance_entry,
)
from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_403_FORBIDDEN,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from attendance.serializers import AttendanceCreateSerializer
import json


class TestManualAttendance(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = generate_test_course()
        self.section = generate_test_section(self.course)
        self.teacher = generate_test_teacher()
        self.students = [generate_test_student() for _ in range(5)]
        self.lecture = generate_test_lecture(self.course, self.section)
        self.section.students.add(*self.students)
        self.course.teachers.add(self.teacher)
        self.section.TAs.add(self.teacher)
        self.course.save()
        self.section.save()
        self.unauthorized_teacher = generate_test_teacher()

    def test_manual_attendance_with_non_teacher(self):
        self.client.force_authenticate(user=self.students[0])
        url = reverse("take-manual-attendance", kwargs={"lecture_id": self.lecture.id})
        data = [{"student": self.students[0].id, "status": 1, "date": "2023-01-01"}]
        data = json.dumps(data)
        response = self.client.post(url, data, content_type="application/json")
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_manual_attendance_with_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        url = reverse("take-manual-attendance", kwargs={"lecture_id": self.lecture.id})
        data = [{"student": self.students[0].id, "status": 1, "date": "2023-01-01"}]
        data = json.dumps(data)
        response = self.client.post(url, data, content_type="application/json")
        assert response.status_code == HTTP_201_CREATED

    def test_manual_attendance_with_non_course_or_section_teacher(self):
        self.client.force_authenticate(user=self.unauthorized_teacher)
        url = reverse("take-manual-attendance", kwargs={"lecture_id": self.lecture.id})
        data = [{"student": self.students[0].id, "status": 1, "date": "2023-01-01"}]
        data = json.dumps(data)
        response = self.client.post(url, data, content_type="application/json")
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_get_lecture_attendance_by_course_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        url = reverse(
            "teacher-lecture-attendance", kwargs={"lecture_id": self.lecture.id}
        )
        response = self.client.get(url)
        assert response.status_code == HTTP_200_OK

    def test_get_lecture_attendance_by_student(self):
        self.client.force_authenticate(user=self.students[0])
        url = reverse(
            "teacher-lecture-attendance", kwargs={"lecture_id": self.lecture.id}
        )
        response = self.client.get(url)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_get_lecture_attendance_by_non_course_teacher(self):
        self.client.force_authenticate(user=self.unauthorized_teacher)
        url = reverse(
            "teacher-lecture-attendance", kwargs={"lecture_id": self.lecture.id}
        )
        response = self.client.get(url)
        assert response.status_code == HTTP_403_FORBIDDEN

    def get_course_attendance_by_course_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        url = reverse("teacher-course-attendance", kwargs={"course_id": self.course.id})
        response = self.client.get(url)
        assert response.status_code == HTTP_200_OK

    def test_get_student_attendance_by_student(self):
        self.client.force_authenticate(user=self.students[0])
        url = reverse("student-attendance")
        response = self.client.get(url)
        assert response.status_code == HTTP_200_OK

    def test_edit_attendance_entry_by_authorized_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        attendance_entry = generate_test_attendance_entry(self.lecture, self.students[0] , "0")
        url = reverse("edit-attendance-entries", kwargs={"lecture_id": self.lecture.id})
        data = [{"student_id": self.students[0].id, "status": "1"}]
        data = json.dumps(data)
        response = self.client.patch(url, data, content_type="application/json")
        assert response.status_code == HTTP_200_OK
        assert response.data[0]["status"] == "1"
        
    def test_edit_attendance_entry_by_unauthorized_teacher(self):
        self.client.force_authenticate(user=self.unauthorized_teacher)
        attendance_entry = generate_test_attendance_entry(self.lecture, self.students[0] , "0")
        url = reverse("edit-attendance-entries", kwargs={"lecture_id": self.lecture.id})
        data = [{"student_id": self.students[0].id, "status": "1"}]
        data = json.dumps(data)
        response = self.client.patch(url, data, content_type="application/json")
        assert response.status_code == HTTP_403_FORBIDDEN
    
    def test_edit_attendance_entry_by_student(self):
        self.client.force_authenticate(user=self.students[0])
        attendance_entry = generate_test_attendance_entry(self.lecture, self.students[0] , "0")
        url = reverse("edit-attendance-entries", kwargs={"lecture_id": self.lecture.id})
        data = [{"student_id": self.students[0].id, "status": "1"}]
        data = json.dumps(data)
        response = self.client.patch(url, data, content_type="application/json")
        assert response.status_code == HTTP_403_FORBIDDEN
