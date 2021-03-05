from django.urls import path, include
from lms_app import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'students', views.StudentViewSets)

app_name = "lms_app"

urlpatterns = [
    path('faculty/', views.FacultyList.as_view()),
    path('subject/', views.SubjectList.as_view()),
    path('lecturer/profile/', views.LecturerProfileList.as_view()),
    path('student/faculty/subjects/', views.StudentFacultySubjectList.as_view()),

    path('subject/detail/<int:pk>/', views.subject_detail),
    path('faculty/detail/<int:pk>/', views.faculty_detail),

    path("", include(router.urls)),
]
