from rest_framework.permissions import BasePermission
from accounts.models import User
from courses.models import Course , Section
from lectures.models import Lecture

TEACHER = "1"
ASSISTANT = "2"


class IsTeacherOrAssistant(BasePermission):
    def has_permission(self, request, view):
        return self.isTeacherOrAssistant(request.user)
    
    def isTeacherOrAssistant(self , user):
        return user and user.is_authenticated and user.role in [TEACHER, ASSISTANT]

class IsCourseTeacher(BasePermission):
    def has_permission(self, request, view ):
        return self.isCourseTeacher(request.user , view.kwargs["course_id"])
    
    def isCourseTeacher(self , user:User , course_id:int ):
        return user and user.is_authenticated and user.role in [TEACHER] and user.courses.filter(id=course_id).exists()
    
class IsSectionTeacher(BasePermission):
    def has_permission(self, request, view ):
        return self.isSectionTeacher(request.user , view.kwargs["section_id"])
    
    def isSectionTeacher(self , user:User , section_id:int ):
        return user and user.is_authenticated and user.role in [TEACHER] and user.sections.filter(id=section_id).exists()

class IsLectureTeacher(BasePermission):
    def has_permission(self, request, view ):
        return self.isLectureTeacher(request.user , view.kwargs["lecture_id"])
    
    def isLectureTeacher(self , user:User , lecture_id:int ):
        lecture: Lecture = Lecture.objects.select_related('course', 'section').get(id=lecture_id)
        course: Course = lecture.course
        section: Section = lecture.section      
        return user and user.is_authenticated and user.role in [TEACHER , ASSISTANT] and course in user.courses.all() if course else section in user.sections.all()

