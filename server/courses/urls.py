from django.urls import path
from .views import (
    CourseListView,
    CourseDetailView,
    CourseCreateView,
    CourseUpdateView,
    SectionCreateView,
    SectionUpdateView,
    TeacherView,
    TAView,
    StudentView,
    enroll_with_join_code

)

app_name = 'courses'

urlpatterns = [
    path('', CourseListView.as_view(), name='course_list'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('create/', CourseCreateView.as_view(), name='course_create'),
    path('<int:pk>/update/', CourseUpdateView.as_view(), name='course_update'),
    path('<int:course_pk>/sections/create/', SectionCreateView.as_view(), name='section_create'),
    path('<int:course_pk>/sections/<int:section_pk>/update/', SectionUpdateView.as_view(), name='section_update'),
    path('<int:course_pk>/teacher/', TeacherView.as_view(), name='teacher'),
    path('<int:section_pk>/ta/', TAView.as_view(), name='ta'),
    path('<int:section_pk>/student/', StudentView.as_view(), name='student'),
    path('enroll/<str:join_code>/', enroll_with_join_code.as_view(), name='enroll_with_join_code'),
]

