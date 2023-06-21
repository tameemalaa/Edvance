from django.urls import path
from .views import(
    AssignmentListView,
    AssignmentDetailView,
    AssignmentCreateView,
    AssignmentUpdateView, 
    AssignmentSubmissionView,
    SubmissionListView,
    GradeCreateView,
    GradeUpdateView,
    GradeDetailView
)

app_name = 'coursework'

urlpatterns = [
    path('assignments/', AssignmentListView.as_view(), name='assignment_list'),
    path('assignments/<int:assignment_pk>/', AssignmentDetailView.as_view(), name='assignment_detail'),
    path('sections/<int:section_pk>/assignments/create/', AssignmentCreateView.as_view(), name='assignment_create'),
    path('assignments/<int:pk>/update/', AssignmentUpdateView.as_view(), name='assignment_update'),
    path('assignments/<int:assignment_pk>/submit/', AssignmentSubmissionView.as_view(), name='assignment_submit'),
    path('assignments/<int:assignment_pk>/submissions/', SubmissionListView.as_view(), name='submission_list'),
    path('submissions/<int:submission_pk>/grade/', GradeCreateView.as_view(), name='grade_create'),
    path('grades/<int:assignment_pk>/update/', GradeUpdateView.as_view(), name='grade-update'),
    path('assignments/<int:assignment_pk>/grade/', GradeDetailView.as_view(), name='grade_detail'),
]

