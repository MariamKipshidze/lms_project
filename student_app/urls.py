from django.urls import path
from student_app import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('student/profile/', views.StudentList.as_view()),
    path('student/profile/<int:pk>/', views.StudentDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)