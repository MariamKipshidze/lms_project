from django.urls import path, include
from lms_app import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'students', views.StudentViewSets)

app_name = "lms_app"

urlpatterns = [
    path('lecturer/profile/', views.LecturerProfileList.as_view()),
    path('student/faculty/subjects/', views.StudentFacultySubjectList.as_view()),

    path('subjects/', views.SubjectViewSets.as_view({'get': 'list'})),
    path('subjects/detail/<int:pk>/', views.SubjectViewSets.as_view({'get': 'retrieve', 'post': 'update'})),

    path('faculty/', views.FacultyViewSets.as_view({'get': 'list'})),
    path('faculty/detail/<int:pk>/', views.FacultyViewSets.as_view({'get': 'retrieve', 'post': 'update'})),

    path("", include(router.urls)),
]
