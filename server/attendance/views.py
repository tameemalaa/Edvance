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


class AttendanceView(generics.CreateAPIView):
    serializer_class = AttendanceListSerializer

    def post(self, request, *args, **kwargs):
        lecture_id = request.data[0].get('lecture')
        serializer = AttendanceSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        url = f"https://{os.environ.get('FRONTEND_URL')}/attendance/{lecture_id}"
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image()
        img_bytes = io.BytesIO()
        img.save(img_bytes)
        img_bytes.seek(0)
        return HttpResponse(img_bytes, content_type='image/png')
    


@never_cache
def qr_code(request, qr_code):
    attendance = Attendance.objects.filter(qr_code=qr_code).first()
    if not attendance:
        return HttpResponseNotFound()
    context = {'qr_code': qr_code}
    return render(request, 'attendance/qr_code.html', context)

class AttendanceScanView(generics.UpdateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def patch(self, request, qr_code, *args, **kwargs):
        attendance = get_object_or_404(Attendance, qr_code=qr_code)
        attendance.status = request.data.get('status', 1)
        attendance.save()
        serializer = self.get_serializer(attendance)
        return Response(serializer.data, status=status.HTTP_200_OK)