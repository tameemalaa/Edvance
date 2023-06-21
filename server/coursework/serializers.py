from rest_framework import serializers
from accounts.serializers import UserSerializer
from courses.serializers import SectionSerializer, CourseSerializer

from .models import Assignment, Submission, Grade


class AssignmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    section = SectionSerializer(read_only=True)
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Assignment
        fields = '__all__'

class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    assignment = AssignmentSerializer(read_only=True)
    student = UserSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = '__all__'


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'
