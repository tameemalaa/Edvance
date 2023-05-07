from rest_framework import serializers
from .models import Course, Section
from accounts.serializers import UserSerializer

class CourseSerializer(serializers.ModelSerializer):
    teachers = UserSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'status', 'created_at', 'updated_at', 'teachers', 'owner']


class SectionSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    TAs = UserSerializer(many=True, read_only=True)
    students = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ['id', 'name', 'description', 'course', 'status', 'created_at', 'updated_at', 'TAs', 'students', 'join_code']
