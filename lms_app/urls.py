from django.urls import path
from lms_app import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "lms_app"

urlpatterns = [
    path('student/profile/', views.StudentList.as_view()),
    path('student/profile/<int:pk>/', views.StudentDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('user/<int:pk>/', views.UserDetail.as_view()),
    path('faculty/', views.FacultyList.as_view()),
    path('subject/', views.SubjectList.as_view()),
    path('lecturer/profile/', views.LecturerProfileList.as_view()),

    path('subject/detail/<int:pk>/', views.subject_detail),
    path('faculty/detail/<int:pk>/', views.faculty_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)