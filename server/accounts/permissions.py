from rest_framework.permissions import BasePermission

TEACHER = "1"
ASSISTANT = "2"


class IsTeacherOrAssistant(BasePermission):
    def has_permission(self, request, view):
        return self.isTeacherOrAssistant(request.user)
    
    def isTeacherOrAssistant(self , user):
        return user and user.is_authenticated and user.role in [TEACHER, ASSISTANT]
