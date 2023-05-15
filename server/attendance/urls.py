from django.urls import path
from .views import (
    GenerateQRAttendance,
    AttendanceScan,
    TeacherManualLectureAttendance,
    StudentAttendance,
    StudentCourseAttendance,
    StudentSectionAttendance,
    TeacherCourseAttendance,
    TeacherSectionAttendance,
    TeacherLectureAttendance,
    AttendanceUpdateStatusView,
)

urlpatterns = [
    path("student/scan/<str:token>", AttendanceScan.as_view(), name="attendance-scan"),
    path("student/", StudentAttendance.as_view(), name="student-attendance"),
    path(
        "student/course/<int:course_id>",
        StudentCourseAttendance.as_view(),
        name="student-course-attendance",
    ),
    path(
        "student/section/<int:section_id>",
        StudentSectionAttendance.as_view(),
        name="student-section-attendance",
    ),
    path(
        "teacher/qr/<int:lecture_id>",
        GenerateQRAttendance.as_view(),
        name="generate-qr-attendance",
    ),
    path(
        "teacher/manual/<int:lecture_id>",
        TeacherManualLectureAttendance.as_view(),
        name="take-manual-attendance",
    ),
    path(
        "teacher/course/<int:course_id>",
        TeacherCourseAttendance.as_view(),
        name="teacher-course-attendance",
    ),
    path(
        "teacher/section/<int:section_id>",
        TeacherSectionAttendance.as_view(),
        name="teacher-section-attendance",
    ),
    path(
        "teacher/lecture/<int:lecture_id>",
        TeacherLectureAttendance.as_view(),
        name="teacher-lecture-attendance",
    ),
    path(
        "teacher/edit/<int:lecture_id>",
        AttendanceUpdateStatusView.as_view(),
        name="edit-attendance-entries",
    ),
]
