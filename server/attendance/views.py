from rest_framework import generics, status
from rest_framework.response import Response
from django.urls import reverse
from django.utils.crypto import get_random_string
from .models import Attendance
from .serializers import AttendanceSerializer , AttendanceListSerializer
from django.shortcuts import get_object_or_404 , render
from django.http import HttpResponseNotFound
from django.views.decorators.cache import never_cache
import qrcode
import io 
import os 
from django.http import HttpResponse
from lectures.models import Lecture 
from courses.models import Course , Section
from rest_framework.views import APIView
from typing import List
from accounts.models import User 
from accounts.permissions import IsTeacherOrAssistant
from rest_framework.permissions import IsAuthenticated 
class GenerateQRAttendance(APIView):
    permission_classes = [IsAuthenticated, IsTeacherOrAssistant]
    def get(self, request, lecture_id):
        lecture : Lecture = get_object_or_404(Lecture, id=lecture_id)

        course : Course = lecture.course
        students :List[User]  = []

        if section := lecture.section:
            students = section.students.all()
        elif course :
            sections = course.section.all()
            for section in sections:
                students.append(section.students.all())

        for student in students:
            attendance, created = Attendance.objects.get_or_create(student=student, lecture=lecture , date = lecture.date )
            if created:
                attendance.status = "0"
                attendance.save()


        url = f"https://{os.environ.get('FRONTEND_URL')}/attendance/{lecture_id}"
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image()
        img_bytes = io.BytesIO()
        img.save(img_bytes)
        img_bytes.seek(0)
        return HttpResponse(img_bytes, content_type='image/png')

class ManualAttendance(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated, IsTeacherOrAssistant]
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    

class AttendanceScanView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self , request , lecture):
        attendance = get_object_or_404(Attendance , lecture = lecture , student = request.user )
        attendance.status = "1"
        attendance.save()
        return Response(status=status.HTTP_200_OK)

