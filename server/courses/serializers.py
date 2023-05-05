from rest_framework import serializers
from .models import Course, Section
from accounts.serializers import UserSerializer


class CourseSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    teachers = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


class SectionSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    TAs = UserSerializer(many=True, read_only=True)
    students = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = '__all__'
