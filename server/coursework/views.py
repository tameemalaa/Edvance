
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.http import require_http_methods
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import Assignment, Submission, Grade
from .serializers import AssignmentSerializer, GradeSerializer, AssignmentSubmissionSerializer
from accounts.models import User
from django.core.exceptions import ObjectDoesNotExist
from courses.models import Course, Section

    
class AssignmentListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.role == "1":
            sections = Section.objects.filter(students=request.user)
            assignments = Assignment.objects.filter(section__in=sections)
            serializer = AssignmentSerializer(assignments, many=True)
            return Response(serializer.data)
        elif request.user.role == "3":
            courses = Course.objects.filter(owner=request.user)
            sections = Section.objects.filter(course__in=courses)
            assignments = Assignment.objects.filter(section__in=sections)
            serializer = AssignmentSerializer(assignments, many=True)
            return Response(serializer.data)
        elif request.user.role == "2":
            sections = Section.objects.filter(TAs=request.user)
            assignments = Assignment.objects.filter(section__in=sections)
            serializer = AssignmentSerializer(assignments, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class AssignmentDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, assignment_pk):
        assignment = get_object_or_404(Assignment, pk=assignment_pk)
        
        # Check if the user is authorized to view the assignment details
        if self.can_view_assignment(request.user, assignment):
            serializer = AssignmentSerializer(assignment)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def can_view_assignment(self, user, assignment):
        # Check if the user has a role that allows them to view the assignment details
        if user.role == "1":
            # Student can view the assignment if they are enrolled in the associated section
            return assignment.section.students.filter(pk=user.pk).exists()
        elif user.role == "3":
            # Teacher can view the assignment if they own the associated course
            return assignment.section.course.owner == user
        elif user.role == "2":
            # TA can view the assignment if they manage the associated section
            return assignment.section.TAs.filter(pk=user.pk).exists()
        else:
            return False


class AssignmentCreateView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, section_pk):
        section = get_object_or_404(Section, pk=section_pk)
        if self.test_func(request.user, section):
            serializer = AssignmentSerializer(data=request.data)
            if serializer.is_valid():
                assignment = serializer.save(section=section, course=section.course, creator=request.user)  # Set the course field
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def test_func(self, user, section):
        return user == section.course.owner or user in section.course.teachers.all() or user in section.TAs.all()


class AssignmentUpdateView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        assignment = get_object_or_404(Assignment, pk=pk)
        if self.test_func(request.user, assignment):
            serializer = AssignmentSerializer(assignment)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request, pk):
        assignment = get_object_or_404(Assignment, pk=pk)
        if self.test_func(request.user, assignment):
            serializer = AssignmentSerializer(assignment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        assignment = get_object_or_404(Assignment, pk=pk)
        if self.test_func(request.user, assignment):
            assignment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def test_func(self, user, assignment):
        return user == assignment.section.course.owner or user in assignment.section.course.teachers.all() or user in assignment.section.TAs.all()




class AssignmentSubmissionView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, assignment_pk):
        assignment = get_object_or_404(Assignment, pk=assignment_pk)
        
        # Check if the user is authorized to submit the assignment
        if self.can_submit_assignment(request.user, assignment):
            # Retrieve the submitted file, text, and link from the request
            submitted_file = request.FILES.get('file')
            text_submission = request.data.get('text_submission')
            link_submission = request.data.get('link_submission')

            # Check if any of the submission fields are provided
            if submitted_file or text_submission or link_submission:
                # Create a new submission object
                submission = Submission.objects.create(
                    assignment=assignment,
                    student=request.user,
                    file=submitted_file,
                    text_submission=text_submission,
                    link_submission=link_submission
                )
                # Perform any additional processing or validation here

                # Return a response indicating successful submission
                return Response({'message': 'Assignment submitted successfully.'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'At least one submission field is required.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        

    def can_submit_assignment(self, user, assignment):
        # Check if the user has a role that allows them to submit the assignment
        if user.role == "1":
            # Student can submit the assignment if they are enrolled in the associated section
            return assignment.section.students.filter(pk=user.pk).exists()
        else:
            return False



class SubmissionListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, assignment_pk):
        assignment = get_object_or_404(Assignment, pk=assignment_pk)
        
        if self.can_view_submissions(request.user, assignment):
            if request.user.role == "1":
                # Student can only view their own submissions
                submissions = Submission.objects.filter(assignment=assignment, student=request.user)
            else:
                submissions = Submission.objects.filter(assignment=assignment)
            
            serializer = AssignmentSubmissionSerializer(submissions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def can_view_submissions(self, user, assignment):
        # Check if the user has a role that allows them to view submissions
        if user.role == "3":
            # Teacher can view submissions if they own the associated course
            return assignment.section.course.owner == user
        elif user.role == "2":
            # TA can view submissions if they manage the associated section
            return assignment.section.TAs.filter(pk=user.pk).exists()
        elif user.role == "1":
            # Student can view their own submissions
            return True
        else:
            return False



class GradeCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, submission_pk):
        submission = get_object_or_404(Submission, pk=submission_pk)
        if self.can_grade_submission(request.user, submission):
            serializer = GradeSerializer(data=request.data)
            if serializer.is_valid():
                grade = serializer.save(submission=submission, grader=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def can_grade_submission(self, user, submission):
        # Check if the user has a role that allows them to grade submissions
        if user.role == "3":
            # Teacher can grade submissions if they own the associated course
            return submission.assignment.section.course.owner == user
        elif user.role == "2":
            # TA can grade submissions if they manage the associated section
            return submission.assignment.section.TAs.filter(pk=user.pk).exists()
        else:
            return False



class GradeUpdateView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, assignment_pk):
        assignment = get_object_or_404(Assignment, pk=assignment_pk)
        grade = Grade.objects.filter(assignment=assignment, submission__student=request.user).first()

        if grade and self.can_update_grade(request.user, grade):
            serializer = GradeSerializer(grade, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def can_update_grade(self, user, grade):
        if user.role == "3":
            # Teacher can update grades if they own the associated course
            return grade.assignment.section.course.owner == user
        elif user.role == "2":
            # TA can update grades if they manage the associated section
            return grade.assignment.section.TAs.filter(pk=user.pk).exists()
        else:
            return False


class GradeDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, assignment_pk):
        assignment = get_object_or_404(Assignment, pk=assignment_pk)
        grade = get_object_or_404(Grade, assignment=assignment)

        if self.can_view_grade(request.user, grade):
            serializer = GradeSerializer(grade)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


    def can_view_grade(self, user, grade):
        if user.role == "1":
            return grade.submission.student == user
        elif user.role == "3":
            return grade.submission.assignment.section.course.owner == user
        elif user.role == "2":
            return grade.submission.assignment.section.TAs.filter(pk=user.pk).exists()
        else:
            return False