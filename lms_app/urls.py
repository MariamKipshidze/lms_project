from django.urls import path, include
from lms_app import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'students', views.StudentViewSets)
router.register(r'lecturer', views.LecturerViewSets)
router.register(r'subjects', views.SubjectViewSets)
router.register(r'faculty', views.FacultyViewSets)

app_name = "lms_app"

urlpatterns = [
    path('student/faculty/subjects/', views.StudentFacultySubjectList.as_view()),

    path('chosen/subjects/', views.StudentChosenSubjectViewSets.as_view({'get': 'list',
                                                                         'post': 'create'})),
    path('chosen/subjects/detail/<int:pk>/', views.StudentChosenSubjectViewSets.as_view({'get': 'retrieve',
                                                                                         'delete': 'destroy'})),

    path('chosen/subjects/update/<int:pk>/', views.ChosenSubjectViewSet.as_view({'get': 'retrieve',
                                                                                 'post': 'update'})),

    path("", include(router.urls)),
]
