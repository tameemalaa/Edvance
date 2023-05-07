from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Course, Section
from .serializers import CourseSerializer, SectionSerializer
from accounts.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView


class CourseListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.role == "3":
            courses = request.user.courses.all()
        elif request.user.role == "2":
            courses = Course.objects.filter(section__TAs=request.user).distinct()
        else:
            courses = Course.objects.filter(section__students=request.user).distinct()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

class CourseDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        if self.test_func(request.user, course):
            serializer = CourseSerializer(course)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)   
    
    def patch(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        if self.test_func2(request.user, course):
            serializer = CourseSerializer(course, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
    def delete(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        if self.test_func3(request.user, course):
            course.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
    def test_func2(self, user, course):
        return user in course.teachers.all()
    
    def test_func3(self, user, course):
        return user == course.owner

    def test_func(self, user, course):
        return user in course.teachers.all() or any(user in section.students.all() for section in course.section_set.all()) or any(user in section.TAs.all() for section in course.section_set.all())

class CourseCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.user.role != "3":
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            course = serializer.save()
            course.teachers.add(request.user)
            course.add_owner(request.user)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
##SECTION

class SectionCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, course_pk):
        course = get_object_or_404(Course, pk=course_pk)
        if request.user.role != "3":
            return Response(status=status.HTTP_403_FORBIDDEN)
        data = request.data
        data['course'] = CourseSerializer(course).data
        serializer = SectionSerializer(data=data)
        if serializer.is_valid():
            section = serializer.save(course=course)
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


class SectionDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, course_pk, section_pk):
        section = get_object_or_404(Section, pk=section_pk, course=course_pk)
        if self.test_func2(request.user, section):
            serializer = SectionSerializer(section)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, course_pk, section_pk):
        section = get_object_or_404(Section, pk=section_pk, course=course_pk)
        if self.test_func(request.user, section):
            serializer = SectionSerializer(section, data=request.data, partial=True)
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
    def test_func2(self, user, section):
        return user in section.course.teachers.all() or user in section.TAs.all() or user in section.students.all() 
    
#ENROLL/ADD/REMOVE

class TeacherView(APIView):
    permission_classes = (IsAuthenticated,)

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
        teacher_id = request.POST.get('teacher_id')
        teacher = get_object_or_404(User, pk=teacher_id)
        if self.test_func2(request.user, course, teacher):
            course.remove_teacher(teacher)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    def test_func(self, user, course):
        return user in course.teachers.all() 
    
    def test_func2(self, user, course, teacher):
        return user in course.teachers.all() and teacher != course.owner and teacher in course.teachers.all()
    

class TAView(APIView):
    permission_classes = (IsAuthenticated,)

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
    

class StudentView(APIView):
    permission_classes = (IsAuthenticated,)

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
        return user in section.course.teachers.all()  or user in section.TAs.all()
    

class enroll_with_join_code(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, join_code):

        try:
            section = Section.objects.get(join_code=join_code)
            section.join_student(request.user)
            return Response(status=status.HTTP_200_OK)
        except Section.DoesNotExist:
            return Response({"error": "Invalid join code"}, status=status.HTTP_400_BAD_REQUEST)



    