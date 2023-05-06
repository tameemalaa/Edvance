from rest_framework import generics, status
from rest_framework.response import Response
from .models import Attendance
from .serializers import AttendanceSerializer , AttendanceListSerializer
from django.shortcuts import get_object_or_404 , render
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
import jwt
import datetime
from datetime import timezone



class GenerateQRAttendance(APIView):
    permission_classes = [IsAuthenticated, IsTeacherOrAssistant]
    def get(self, request, lecture_id):
        lecture : Lecture = get_object_or_404(Lecture, id=lecture_id)

        course : Course = lecture.course
        section : Section = lecture.section
        students :List[User]  = section.students.all() if section else course.students.all()

        for student in students:
            attendance, created = Attendance.objects.get_or_create(student=student, lecture=lecture , date = lecture.date )
            if created:
                attendance.status = "0"
                attendance.save()

        img_bytes = self.generate_QR_Code(lecture_id , request.GET.get("expire_time_in_minutes" , 5))
        return HttpResponse(img_bytes, content_type='image/png')
    
    def generate_QR_Code(self , lecture_id , expire_time_in_minutes = 5): 
        payload = {
        "lecture_id": lecture_id,
        "exp": datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(seconds=expire_time_in_minutes*60)
        }
        secret = os.environ.get("SECRET_KEY")
        token = jwt.encode(payload, secret, algorithm="HS256")
        url = f"https://{os.environ.get('FRONTEND_URL')}/token/{token}"
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image()
        img_bytes = io.BytesIO()
        img.save(img_bytes)
        img_bytes.seek(0)
        return img_bytes
            

class ManualAttendance(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsTeacherOrAssistant]
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    

class AttendanceScanView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self , request , token):
        try : 
            payload = jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms=["HS256"])
        except jwt.InvalidTokenError:
            return Response(status=status.HTTP_401_UNAUTHORIZED , data = {"message" : "Invalid Token"})
        
        lecture = get_object_or_404(Lecture , id = payload["lecture_id"])
        attendance = get_object_or_404(Attendance , lecture = lecture , student = request.user )
        attendance.status = "1"
        attendance.save()
        return Response(status=status.HTTP_200_OK)

class AttendanceListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceListSerializer
    def get_queryset(self):
        return Attendance.objects.filter(student = self.request.user)
    

