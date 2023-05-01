from django.urls import path
from .views import GenerateQRAttendance, AttendanceScanView , ManualAttendance

urlpatterns = [
    path('attendance/qr/<int:lecture_id>', GenerateQRAttendance.as_view(), name='attendance-qr'),
    path('attendance/scan/<str:lecture_id>/', AttendanceScanView.as_view(), name='attendance-scan') , 
    path('attendance/manual/', ManualAttendance.as_view(), name='attendance-manual')
]