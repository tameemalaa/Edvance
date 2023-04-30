from django.urls import path
from .views import AttendanceView, AttendanceScanView, qr_code

urlpatterns = [
    path('attendance/qr/', AttendanceView.as_view(), name='attendance-qr'),
    path('attendance/qr/<str:qr_code>/', qr_code, name='attendance-qr-code'),
    path('attendance/scan/<str:qr_code>/', AttendanceScanView.as_view(), name='attendance-scan'),
]