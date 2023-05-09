from rest_framework.permissions import BasePermission
from accounts.models import User
from courses.models import Course, Section
from lectures.models import Lecture

TEACHER = "1"
ASSISTANT = "2"


class IsTeacherOrAssistant(BasePermission):
    message = "The user is not a teacher or assistant."
    def has_permission(self, request, view):
        return self.is_teacher_or_assistant(request.user)

    def is_teacher_or_assistant(self, user):
        return user and user.is_authenticated and user.role in [TEACHER, ASSISTANT]


class IsCourseTeacher(BasePermission):
    message = "The user is not the teacher of this course."
    def has_permission(self, request, view):
        return self.is_course_teacher(request.user, view.kwargs["course_id"])

    def is_course_teacher(self, user: User, course_id: int):
        return (
            user
            and user.is_authenticated
            and user.role in [TEACHER]
            and user.courses.filter(id=course_id).exists()
        )


class IsSectionTeacher(BasePermission):
    message = "The user is a the teacher of this section."
    def has_permission(self, request, view):
        return self.is_section_teacher(request.user, view.kwargs["section_id"])

    def is_section_teacher(self, user: User, section_id: int):
        return (
            user
            and user.is_authenticated
            and user.role in [TEACHER]
            and user.sections.filter(id=section_id).exists()
        )

class IsLectureTeacher(BasePermission):
    message = "The user is not the teacher of this lecture."
    def has_permission(self, request, view):
        return self.is_lecture_teacher(request.user, view.kwargs["lecture_id"])

    def is_lecture_teacher(self, user: User, lecture_id: int):
        lecture: Lecture = Lecture.objects.select_related("course", "section").get(
            id=lecture_id
        )
        course: Course = lecture.course
        section: Section = lecture.section
        return (
            user
            and user.is_authenticated
            and user.role in [TEACHER, ASSISTANT]
            and course in user.courses.all()
            if course
            else section in user.sections.all()
        )
