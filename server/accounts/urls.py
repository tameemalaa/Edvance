from django.urls import path
from .views import UserUpdateView

urlpatterns = [
    path('users/me/', UserUpdateView.as_view(), name='user_update'),
]