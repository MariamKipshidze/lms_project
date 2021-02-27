from django.urls import path
from student_app import views

urlpatterns = [
    path('student/profile/', views.student_profile_list),
]