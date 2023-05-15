from django.test import TestCase 
from rest_framework.test import APIClient
from attendance.serializers import AttendanceSerializer 
from util import generate_test_course, generate_test_student, generate_test_teacher , generate_test_TA , generate_test_section , generate_test_lecture
from django.urls import reverse

class TestManualAttendance(TestCase):

    def setup(self): 
        self.client = APIClient()
        self.course = generate_test_course()
        self.section = generate_test_section(self.course)
        self.teacher = generate_test_teacher()
        self.students = [generate_test_student() for _ in range(5)]
        self.lecture = generate_test_lecture(self.course , self.section)
        self.section.students.add(*self.students)
        
    
    def test_manual_attendance_with_non_teacher(self): 
        self.client.force_authenticate(user=self.students[0])    
        url = reverse('take-manual-attendance', kwargs={'lecture_id': self.lecture.id})
        response = self.client.post(url , {'student_id' : self.students[0].id})
        
