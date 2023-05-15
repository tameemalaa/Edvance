from rest_framework import serializers
from .models import Attendance , ABSENCE_STATUS_CHOICES
from django.shortcuts import get_object_or_404
from lectures.models import Lecture
from accounts.models import User 



class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    course_name = serializers.CharField(source='lecture.course.name', read_only=True)
    class Meta:
        model = Attendance
        fields = ( "student_name", "course_name" ,"student" ,  "date", "status" , "lecture" )
        


class AttendanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ("student", "lecture", "date", "status")
        read_only_fields = ( "lecture",)
    
    def create(self, validated_data):
        lecture_id = self.context['request'].parser_context['kwargs']['lecture_id']
        lecture = get_object_or_404(Lecture, id=lecture_id)
        instance = Attendance.objects.create(lecture = lecture, **validated_data)
        return instance
    

class AttendanceCreateListSerializer(serializers.ListSerializer):
    child = AttendanceCreateSerializer()


class AttendancePartialUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    status = serializers.ChoiceField(choices=ABSENCE_STATUS_CHOICES)
    class Meta:
        list_serializer_class = serializers.ListSerializer
    
class AttendanceListPartialUpdateSerializer(serializers.ListSerializer): 
    child=AttendancePartialUpdateSerializer()
    