from rest_framework import generics, status
from rest_framework.response import Response
from .models import Attendance
from .serializers import (
    AttendanceSerializer,
    AttendancePartialUpdateSerializer,
    AttendanceListPartialUpdateSerializer,
    AttendanceCreateSerializer ,
    )
from django.shortcuts import get_object_or_404
import qrcode
import io
import os
from django.http import HttpResponse
from lectures.models import Lecture
from courses.models import Course, Section
from rest_framework.views import APIView
from typing import List
from accounts.models import User
from accounts.permissions import IsTeacherOrAssistant , IsCourseTeacher , IsSectionTeacher , IsLectureTeacher
from rest_framework.permissions import IsAuthenticated
import jwt
import datetime
from datetime import timezone
from django.shortcuts import get_object_or_404



class GenerateQRAttendance(APIView):
    permission_classes = [IsAuthenticated, IsLectureTeacher]

    def get(self, request, lecture_id):
        lecture: Lecture = get_object_or_404(Lecture, id=lecture_id)
        course: Course = lecture.course
        section: Section = lecture.section


        students: List[User] = (
            section.students.all() if section else course.students.all()
        )

        for student in students:
            attendance, created = Attendance.objects.get_or_create(
                student=student, lecture=lecture, date=lecture.date
            )
            if created:
                attendance.status = "0"
                attendance.save()

        img_bytes = self.generate_QR_Code(
            lecture_id, request.GET.get("expire_time_in_minutes", 5)
        )
        return HttpResponse(img_bytes, content_type="image/png")

    def generate_QR_Code(self, lecture_id, expire_time_in_minutes=5):
        payload = {
            "lecture_id": lecture_id,
            "exp": datetime.datetime.now(tz=timezone.utc)
            + datetime.timedelta(seconds=int(expire_time_in_minutes) * 60),
        }
        secret = os.environ.get("SECRET_KEY")
        token = jwt.encode(payload, secret, algorithm="HS256")
        url = f"https://{os.environ.get('FRONTEND_URL')}/token/{token}"
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image()
        img_bytes = io.BytesIO()
        img.save(img_bytes , "PNG")
        img_bytes.seek(0)
        return img_bytes


class AttendanceScan(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, token):
        try:
            payload = jwt.decode(
                token, os.environ.get("SECRET_KEY"), algorithms=["HS256"]
            )
        except jwt.InvalidTokenError:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED, data={"message": "Invalid Token"}
            )

        attendance = Attendance.objects.filter(
            student=request.user, lecture__id=payload["lecture_id"]
        ).first()
        attendance.status = "1"
        attendance.save()
        return Response(status=status.HTTP_200_OK)


class TeacherManualLectureAttendance(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsLectureTeacher]
    serializer_class = AttendanceCreateSerializer
    queryset = Attendance.objects.all()
    
    def post(self , request , *args , **kwargs):
        data = request.data
        if not isinstance(data, list):
            data = [data]

        serializer = self.get_serializer(data=data, many=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        



class StudentAttendance(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        return Attendance.objects.filter(student=self.request.user)


class StudentCourseAttendance(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        course_id = self.kwargs["course_id"]
        return Attendance.objects.filter(
            student=self.request.user, lecture__course__id=course_id
        )


class StudentSectionAttendance(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        section_id = self.kwargs["section_id"]
        return Attendance.objects.filter(
            student=self.request.user, lecture__section__id=section_id
        )


class TeacherCourseAttendance(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsCourseTeacher]
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        course_id = self.kwargs["course_id"]
        return Attendance.objects.filter(lecture__course__id=course_id)


class TeacherSectionAttendance(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsSectionTeacher]
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        section_id = self.kwargs["section_id"]
        return Attendance.objects.filter(lecture__section__id=section_id)


class TeacherLectureAttendance(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsLectureTeacher]
    serializer_class = AttendanceSerializer
    
    def get_queryset(self):
        lecture_id = self.kwargs["lecture_id"]
        return Attendance.objects.filter(lecture__id=lecture_id)




class AttendanceUpdateStatusView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsLectureTeacher]
    serializer_class = AttendanceListPartialUpdateSerializer
    
    def get_queryset(self):
        lecture_id = self.kwargs["lecture_id"]
        return Attendance.objects.filter(lecture__id=lecture_id)
    
    def patch(self, request, *args , **kwargs):
        attendance_data = request.data

        if not isinstance(attendance_data, list):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        update_request_serializer = self.get_serializer(data=attendance_data)

        if not update_request_serializer.is_valid():
            return Response(update_request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        updated_attendances = []
        for attendance_entry in update_request_serializer.validated_data:
            pk = attendance_entry["id"]
            status_update = attendance_entry["status"]

            attendance = get_object_or_404(Attendance, pk=pk)
            attendance.status = status_update
            attendance.save()
            updated_attendances.append(attendance)

        response_serializer = AttendanceSerializer(updated_attendances, many=True)
        return Response(response_serializer.data)
        
        
        
