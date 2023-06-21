from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.http import require_http_methods
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Course, Section
from .serializers import CourseSerializer, SectionSerializer
from ..accounts.models import User
from django.core.exceptions import ObjectDoesNotExist


@method_decorator(login_required, name='dispatch')
class CourseListView(View):
    def get(self, request):
        if request.user.role == "3":
            courses = request.user.courses.all()
        elif request.user.role == "2":
            courses = Course.objects.filter(managed_sections=request.user)
        else:
            courses = Course.objects.filter(section_enrollment=request.user)

        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

@method_decorator(login_required, name='dispatch')
class CourseDetailView(View):
    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        if self.test_func(request.user, course):
            serializer = CourseSerializer(course)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def test_func(self, user, course):
        return user in course.teachers.all() or user in course.section.students.all() or user in course.section.TAs.all()

@method_decorator(login_required, name='dispatch')
class CourseCreateView(View):
    def post(self, request):
        if request.user.role != "3":
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            course = serializer.save()
            course.teachers.add(request.user)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(login_required, name='dispatch')
class CourseUpdateView(View):
    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        if self.test_func(request.user, course):
            serializer = CourseSerializer(course)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        if self.test_func(request.user, course):
            serializer = CourseSerializer(course, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
    def delete(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        if self.test_func(request.user, course):
            course.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        

    def test_func(self, user, course):
        return user in course.teachers.all()



##SECTION

@method_decorator(login_required, name='dispatch')
class SectionCreateView(View):
    def post(self, request, course_pk):
        course = get_object_or_404(Course, pk=course_pk)
        if request.user.role != "3":
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = SectionSerializer(data=request.data)
        if serializer.is_valid():
            section = serializer.save(course=course)
            # Retrieve TA object by email
            TA_email = request.data.get('TA_email')
            if TA_email:
                try:
                    TA = User.objects.get(email=TA_email, role="2")
                    section.TAs.add(TA)
                except ObjectDoesNotExist:
                    return Response({"error": "The specified TA does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(login_required, name='dispatch')
class SectionUpdateView(View):
    def get(self, request, course_pk, section_pk):
        section = get_object_or_404(Section, pk=section_pk, course=course_pk)
        if self.test_func(request.user, section):
            serializer = SectionSerializer(section)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request, course_pk, section_pk):
        section = get_object_or_404(Section, pk=section_pk, course=course_pk)
        if self.test_func(request.user, section):
            serializer = SectionSerializer(section, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        

    def delete(self, request, course_pk, section_pk):
        section = get_object_or_404(Section, pk=section_pk, course=course_pk)
        if self.test_func(request.user, section):
            section.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def test_func(self, user, section):
        return user in section.course.teachers.all()
    
#ENROLL/ADD/REMOVE
@method_decorator(login_required, name='dispatch')
class TeacherView(View):
    def post(self, request, course_pk):
        course = get_object_or_404(Course, pk=course_pk)
        if self.test_func(request.user, course):
            teacher_email = request.POST.get('teacher_email')
            teacher = get_object_or_404(User, email=teacher_email)
            course.add_teacher(teacher)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    def delete(self, request, course_pk):
        course = get_object_or_404(Course, pk=course_pk)
        if self.test_func(request.user, course):
            course = get_object_or_404(Course, pk=course_pk)
            teacher_id = request.POST.get('teacher_id')
            teacher = get_object_or_404(User, pk=teacher_id)
            course.remove_teacher(teacher)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    def test_func(self, user, course):
        return user in course.teachers.all()
    
@method_decorator(login_required, name='dispatch')
class TAView(View):
    def post(self, request, section_pk):
        section = get_object_or_404(Section, pk=section_pk)
        if self.test_func(request.user, section):
            TA_email = request.POST.get('TA_email')
            TA = get_object_or_404(User, email=TA_email)
            section.add_TA(TA)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    def delete(self, request, section_pk):
        section = get_object_or_404(Section, pk=section_pk)
        if self.test_func(request.user, section):
            section = get_object_or_404(Section, pk=section_pk)
            TA_id = request.POST.get('TA_id')
            TA = get_object_or_404(User, pk=TA_id)
            section.remove_TA(TA)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    def test_func(self, user, section):
        return user in section.course.teachers.all() or user in section.TAs.all()
    
@method_decorator(login_required, name='dispatch')
class StudentView(View):
    def post(self, request, section_pk):
        section = get_object_or_404(Section, pk=section_pk)
        if self.test_func(request.user, section):
            student_email = request.POST.get('student_email')
            student = get_object_or_404(User, email=student_email)
            section.add_student(student)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    def delete(self, request, section_pk):
        section = get_object_or_404(Section, pk=section_pk)
        if self.test_func(request.user, section):
            section = get_object_or_404(Section, pk=section_pk)
            student_id = request.POST.get('student_id')
            student = get_object_or_404(User, pk=student_id)
            section.remove_student(student)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def test_func(self, user, section):
        return user in section.course.teachers.all()
    
@method_decorator(login_required, name='dispatch')
class enroll_with_join_code(View):
    def post(self, request, join_code):
        try:
            Section.join_student(request.user, join_code)
        except Exception:
            return Response({"error": "Invalid join code"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


    