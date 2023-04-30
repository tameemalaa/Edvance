from rest_framework import serializers
from .models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    course_name = serializers.CharField(source='lecture.course.name', read_only=True)
    class Meta:
        model = Attendance
        fields = ( "student_name", "course_name" ,"student" ,  "date", "status" , "lecture" )

class AttendanceListSerializer(serializers.ListSerializer): 
    child = AttendanceSerializer()